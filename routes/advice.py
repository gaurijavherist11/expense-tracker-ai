import os
import time
import random
from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from flask_login import current_user, login_required
from db import db
from models.advice import FinancialAdvice
from models.income import Income
from models.expense import Expense
from datetime import datetime, timedelta
import requests


advice_blueprint = Blueprint('advice', __name__)

MIN_SECONDS_BETWEEN_GENERATIONS = 30


def generate_with_backoff(model_str, prompt, max_retries=3):
    wait = 1.0
    last_exc = None
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(model_str)
            resp = model.generate_content(prompt)

            text = getattr(resp, "text", None)
            if text is None and isinstance(resp, dict):
                if "candidates" in resp and resp["candidates"]:
                    c = resp["candidates"][0]
                    text = c.get("output") or c.get("content") or c.get("text")
                elif "output" in resp:
                    text = resp["output"]

            if text is None:
                text = str(resp)

            return text.strip()

        except Exception as e:
            last_exc = e
            msg = str(e).lower()

            if "quota" in msg or "429" in msg or "rate" in msg:
                time.sleep(wait + random.random() * 0.5)
                wait *= 2
                continue

            if "404" in msg or "not found" in msg:
                raise

            time.sleep(wait + random.random() * 0.5)
            wait *= 2

    raise last_exc if last_exc else RuntimeError("generate retries exhausted")


def rule_based_advice(total_income, total_expenses, surplus):
    advice_lines = []

    if total_income <= 0:
        advice_lines.append("Income seems zero or not recorded. Track income first.")
    else:
        ratio = total_expenses / total_income if total_income else 1.0

        if ratio >= 1.0:
            advice_lines.append("You are overspending. Cut unnecessary expenses.")
        elif ratio > 0.7:
            advice_lines.append("Expenses are high. Reduce subscriptions and eating out.")
        else:
            advice_lines.append("Good control. Increase savings and investments.")

    advice_lines.append("Track expenses weekly and set limits.")

    return "\n".join(advice_lines)


def get_recent_advice_for_user(user_id, max_age_hours=24):
    cutoff = datetime.now() - timedelta(hours=max_age_hours)
    return FinancialAdvice.query.filter(
        FinancialAdvice.user_id == user_id,
        FinancialAdvice.generated_date >= cutoff
    ).order_by(FinancialAdvice.generated_date.desc()).first()


def generate_with_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:latest",
            "prompt": prompt,
            "stream": False
        },
        timeout=8
    )
    return response.json()["response"]


@advice_blueprint.route('/generate', methods=['GET', 'POST'])
@login_required
def generate_advice():
    if request.method == 'POST':

        incomes = Income.query.filter_by(user_id=current_user.id).all()
        expenses = Expense.query.filter_by(user_id=current_user.id).all()

        total_income = sum([i.amount for i in incomes]) if incomes else 0
        total_expenses = sum([e.amount for e in expenses]) if expenses else 0
        surplus = total_income - total_expenses

        prompt = f"Income:{total_income}, Expenses:{total_expenses}, Surplus:{surplus}"

        try:
            advice_text = generate_with_ollama(prompt)
        except Exception:
            advice_text = rule_based_advice(total_income, total_expenses, surplus)

        new_advice = FinancialAdvice(
            user_id=current_user.id,
            advice_text=advice_text,
            generated_date=datetime.now()
        )
        db.session.add(new_advice)
        db.session.commit()

        advice_text_html = advice_text.replace('\n', '<br>')

        return render_template(
            'dashboard.html',
            active_tab='advice',
            advice=advice_text_html
        )

    return render_template('dashboard.html', active_tab='advice')


@advice_blueprint.route('/chat', methods=['POST'])
@login_required
def chat_with_ollama():
    user_message = request.form.get('message')

    if 'chat_history' not in session:
        session['chat_history'] = []

    # Add user message
    session['chat_history'].append({"role": "user", "content": user_message})

    # Build conversation
    conversation = ""
    for msg in session['chat_history']:
        conversation += f"{msg['role']}: {msg['content']}\n"

    try:
        reply = generate_with_ollama(conversation)
    except Exception as e:
        print("Ollama failed:", e)
        reply = "⚡ Quick advice: Reduce unnecessary spending, track expenses, and save regularly."

    # ✅ REMOVE ONLY LAST USER MESSAGE (FIX)
    if session['chat_history'] and session['chat_history'][-1]['role'] == 'user':
        session['chat_history'].pop()

    # Add assistant reply
    session['chat_history'].append({"role": "assistant", "content": reply})

    return render_template(
        'dashboard.html',
        active_tab='advice',
        chat_history=session['chat_history']
    )


@advice_blueprint.route('/chat/clear')
def clear_chat():
    session.pop('chat_history', None)
    return redirect(url_for('view_data.view_data'))