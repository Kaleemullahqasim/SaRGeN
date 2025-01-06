import pandas as pd
import streamlit as st

class TransactionProcessor:
    @staticmethod
    def load_data(file):
        try:
            data = pd.read_csv(file)
            data['date'] = pd.to_datetime(data['date'])
            return data
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None

    @staticmethod
    def preprocess_transactions(data):
        # Add preprocessing steps here
        # Example:
        data['month'] = data['date'].dt.month
        data['day'] = data['date'].dt.day
        data['weekday'] = data['date'].dt.weekday
        return data

    @staticmethod
    def get_customer_summary(data, customer_id):
        customer_data = data[data['customer_id'] == customer_id]
        summary = {
            'total_transactions': len(customer_data),
            'total_amount': customer_data['amount'].sum(),
            'avg_transaction': customer_data['amount'].mean(),
            'transaction_types': customer_data['type'].value_counts().to_dict()
        }
        return summary
