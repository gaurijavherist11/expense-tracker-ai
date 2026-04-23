import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Function to preprocess the uploaded CSV file
def preprocess_data(file):
    data = pd.read_csv(file)
    # Ensure the Date column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Check for required columns
    required_columns = ['Date', 'Description', 'Amount', 'Type']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Add a Month column for monthly aggregation
    data['Month'] = data['Date'].dt.to_period('M')
    return data

# Function to analyze monthly data
def analyze_monthly(data):
    # Aggregate income and expenses by month
    monthly_data = data.pivot_table(
        values='Amount',
        index='Month',
        columns='Type',
        aggfunc='sum',
        fill_value=0
    )
    monthly_data['Savings'] = monthly_data.get('Credit', 0) - monthly_data.get('Debit', 0)
    return monthly_data

# Function to track expenses by category
def track_expenses(data):
    # Group by categories and calculate total spending
    if 'Category' not in data.columns:
        def categorize(description):
            if "grocer" in description.lower():
                return "Groceries"
            elif "rent" in description.lower():
                return "Rent"
            elif "bill" in description.lower() or "electric" in description.lower():
                return "Utilities"
            elif "dining" in description.lower() or "travel" in description.lower():
                return "Entertainment"
            elif "subscription" in description.lower() or "membership" in description.lower():
                return "Subscriptions"
            elif "shopping" in description.lower():
                return "Shopping"
            elif "salary" in description.lower():
                return "Income"
            else:
                return "Other"
        data['Category'] = data['Description'].apply(categorize)
    category_expenses = data[data['Type'] == 'Debit'].groupby('Category')['Amount'].sum().sort_values(ascending=False)
    return category_expenses

# Function to generate recommendations
def generate_recommendations(category_expenses):
    recommendations = []
    for category, amount in category_expenses.items():
        if amount > 1000:  # Adjust threshold for high spending
            recommendations.append(f"Consider reducing spending on {category} (₹{amount:.2f}).")
    if not recommendations:
        recommendations.append("Your spending is well-managed. Keep it up!")
    return recommendations

# Streamlit app
def main():
    st.title("Personal Expense Tracker and Recommendation System")

    # File upload
    uploaded_file = st.file_uploader("Upload your bank statement (CSV)", type=["csv"])
    if uploaded_file is not None:
        try:
            # Preprocess and analyze the data
            data = preprocess_data(uploaded_file)
            st.success("File uploaded and processed successfully!")

            # Monthly analysis
            st.subheader("Monthly Analysis")
            monthly_data = analyze_monthly(data)
            st.dataframe(monthly_data)

            # Plot monthly income, expenses, and savings
            st.subheader("Monthly Income, Expenses, and Savings")
            fig, ax = plt.subplots(figsize=(10, 6))
            monthly_data.plot(kind='bar', ax=ax)
            plt.title("Monthly Analysis")
            plt.ylabel("Amount (₹)")
            plt.xlabel("Month")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Expense tracking
            st.subheader("Category-Wise Expense Tracking")
            category_expenses = track_expenses(data)
            st.dataframe(category_expenses)

            # Plot category expenses
            fig, ax = plt.subplots(figsize=(10, 6))
            category_expenses.plot(kind='bar', color='orange', ax=ax)
            plt.title("Spending by Category")
            plt.ylabel("Amount (₹)")
            plt.xlabel("Category")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Recommendations
            st.subheader("Recommendations")
            recommendations = generate_recommendations(category_expenses)
            for rec in recommendations:
                st.write("- ", rec)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Please upload a CSV file to begin.")

if __name__ == "__main__":
    main()
