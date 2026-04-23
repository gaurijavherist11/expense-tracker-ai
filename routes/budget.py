from flask import Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required
from db import db
from models.budget import Budget
from datetime import datetime

budget_blueprint = Blueprint('budget', __name__)

@budget_blueprint.route('/add', methods=['POST'])
@login_required
def add_budget():
    category = request.form.get('category')
    amount = request.form.get('amount')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if not category or not amount or not start_date or not end_date:
        flash("All fields are required!", "danger")
        return redirect(url_for('index'))

    try:
        new_budget = Budget(
            user_id=current_user.id,
            category=category,
            amount=float(amount),
            start_date=datetime.strptime(start_date, '%Y-%m-%d'),
            end_date=datetime.strptime(end_date, '%Y-%m-%d')
        )
        db.session.add(new_budget)
        db.session.commit()
        flash("Budget added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding budget: {str(e)}", "danger")

    return redirect(url_for('view_data.view_data'))
