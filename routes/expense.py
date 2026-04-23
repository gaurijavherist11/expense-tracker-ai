from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from flask_login import current_user, login_required
from db import db
from models.expense import Expense
from datetime import datetime
from .ollama_helper import ask_ollama

expense_blueprint = Blueprint('expense', __name__)


@expense_blueprint.route('/add', methods=['POST'])
@login_required
def add_expense():
    try:
        # Get form data
        amount = request.form.get('amount')
        category = request.form.get('category')
        date_spent = request.form.get('date')
        regret_value = request.form.get('regret')

        # Validate required fields
        if not amount or not category or not date_spent:
            flash("All fields are required!", "danger")
            return redirect(url_for('index'))

        # Create expense object
        new_expense = Expense(
            user_id=current_user.id,
            amount=float(amount),
            category=category,
            date_spent=datetime.strptime(date_spent, '%Y-%m-%d'),
            regret=int(regret_value) if regret_value else None
        )

        # Save to DB
        db.session.add(new_expense)
        db.session.commit()

        # 🔹 REAL AI ADVICE USING OLLAMA
        prompt = f"""
You are a financial assistant.

A user just added an expense:
- Amount: {amount} rupees
- Category: {category}
- Date: {date_spent}

Explain in very simple and kind language
why the user should think before spending like this.
Do not judge.
Give one gentle suggestion.
Keep it short.
"""
        session['ai_advice'] = ask_ollama(prompt)

        flash("Expense added successfully!", "success")
        return redirect(url_for('view_data.view_data'))

    except Exception as e:
        db.session.rollback()
        print("Error adding expense:", e)
        flash(f"Error adding expense: {str(e)}", "danger")
        return redirect(url_for('index'))


@expense_blueprint.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for('view_data.view_data'))


@expense_blueprint.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if request.method == 'POST':
        expense.amount = float(request.form.get('amount'))
        expense.category = request.form.get('category')
        expense.date_spent = datetime.strptime(
        request.form.get('date'), '%Y-%m-%d'
        )

        regret_value = request.form.get('regret')
        expense.regret = int(regret_value) if regret_value else None


        # ✅ NEW — update feedback also
        regret_value = request.form.get('regret')
        expense.regret = int(regret_value) if regret_value else None

        db.session.commit()
        flash("Expense updated successfully!", "success")
        return redirect(url_for('view_data.view_data'))

    return render_template('edit_expense.html', expense=expense)
