from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from datetime import datetime

from db import db
from models.income import Income
from datetime import datetime
from flask import render_template



# Define the blueprint for income routes
income_blueprint = Blueprint('income', __name__)

@income_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_income():

    # =====================
    # GET REQUEST → SHOW FORM
    # =====================
    if request.method == 'GET':
        return render_template('add_income.html')

    # =====================
    # POST REQUEST → SAVE DATA
    # =====================
    amount = request.form.get('amount')
    source = request.form.get('source')
    date_received = request.form.get('date')

    # Debug logs
    print("Income Details - Amount:", amount, "Source:", source, "Date:", date_received)
    print("Current User ID:", current_user.id)

    # Validation
    if not amount or not date_received:
        flash("Amount and date are required!", "danger")
        return redirect(url_for('income.add_income'))

    try:
        new_income = Income(
            user_id=current_user.id,
            amount=float(amount),
            source=source,
            date_received=datetime.strptime(date_received, '%Y-%m-%d')
        )

        db.session.add(new_income)
        db.session.commit()
        flash("Income added successfully!", "success")

    except Exception as e:
        db.session.rollback()
        print("Error adding income:", e)
        flash("Error adding income. Please try again.", "danger")

    # Redirect after success
    return redirect(url_for('view_data.view_data'))

#delete income
@income_blueprint.route('/delete/<int:income_id>', methods=['POST'])
@login_required
def delete_income(income_id):
    income = Income.query.get_or_404(income_id)
    db.session.delete(income)
    db.session.commit()
    flash("Income deleted successfully!", "success")
    return redirect(url_for('view_data.view_data'))


#Edit income 
@income_blueprint.route('/edit/<int:income_id>', methods=['GET', 'POST'])
@login_required
def edit_income(income_id):
    income = Income.query.get_or_404(income_id)

    if request.method == 'POST':
        income.amount = float(request.form.get('amount'))
        income.source = request.form.get('source')
        income.date_received = datetime.strptime(
            request.form.get('date'), '%Y-%m-%d'
        )
        db.session.commit()
        flash("Income updated successfully!", "success")
        return redirect(url_for('view_data.view_data'))

    return render_template('edit_income.html', income=income)

