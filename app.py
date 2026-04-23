from flask import Flask, render_template
from config import Config
from db import db
from routes.auth import auth_blueprint
from routes.income import income_blueprint
from flask_login import LoginManager
from models.user import User  # Import your User model
from routes.expense import expense_blueprint
from routes.view_data import view_data_blueprint
from routes.budget import budget_blueprint
from routes.advice import advice_blueprint


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Set the login view (redirects unauthorized users here)
login_manager.login_view = 'auth.login'  # Match this to the login route's endpoint
login_manager.login_message_category = 'danger'

# Define user loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(income_blueprint, url_prefix='/income')
app.register_blueprint(expense_blueprint, url_prefix='/expense')
app.register_blueprint(view_data_blueprint, url_prefix='/data')
app.register_blueprint(budget_blueprint, url_prefix='/budget')
app.register_blueprint(advice_blueprint, url_prefix='/advice')



# Home route
@app.route('/')
def index():
    return render_template('dashboard.html')

# Main entry point
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # 🔥 THIS LINE FIXES YOUR ERROR
    app.run(debug=True)