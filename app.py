import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# from sar_generator import generate_sar_narrative
from sar_groq import generate_sar_narrative
from red_flag_rules import (detect_high_value_cash_deposits, detect_structured_transactions,
                            detect_high_risk_country_transactions,
                             detect_high_velocity_cash_activity,
                            detect_keywords_hitting, detect_unusual_transaction_patterns,
                            detect_large_incoming_wires)

# Data Processing Module
def load_data(file):
    try:
        data = pd.read_csv(file)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Red Flag Rules Module
def apply_red_flag_rules(transactions, selected_rules, customer_id=None):
    rules = {
        'high_value_cash_deposits': detect_high_value_cash_deposits,
        'structured_transactions': detect_structured_transactions,
        'high_risk_country_transactions': detect_high_risk_country_transactions,
        # 'rapid_movement_of_funds': detect_rapid_movement_of_funds,
        # 'inconsistent_business_activity': detect_inconsistent_business_activity,
        'high_velocity_cash_activity': detect_high_velocity_cash_activity,
        'keywords_hitting': detect_keywords_hitting,
        'unusual_transaction_patterns': detect_unusual_transaction_patterns,
        # 'commingling_of_funds': detect_commingling_of_funds,
        'large_incoming_wires': detect_large_incoming_wires,
    }

    flagged_transactions = {}
    for rule_name in selected_rules:
        if rule_name in rules:
            if customer_id:
                customer_transactions = transactions[transactions['customer_id'] == customer_id]
                flagged_transactions[rule_name] = rules[rule_name](customer_transactions)
            else:
                flagged_transactions[rule_name] = rules[rule_name](transactions)
    
    return flagged_transactions

# Function to get customers with multiple rule violations
def get_customers_with_multiple_violations(flagged_transactions):
    customer_violations = {}
    for rule, dataset in flagged_transactions.items():
        for customer_id in dataset['customer_id']:
            if customer_id not in customer_violations:
                customer_violations[customer_id] = set()
            customer_violations[customer_id].add(rule)
    return {customer: rules for customer, rules in customer_violations.items() if len(rules) > 1}

# Streamlit App
st.set_page_config(page_title="BSA / AML Detection System", layout="wide")
st.title("BSA / AML Detection System")

# Sidebar for file upload and options
with st.sidebar:
    st.header("Upload and Options")
    uploaded_file = st.file_uploader("Upload Transaction Data (CSV)", type=["csv"])
    option = st.selectbox("Choose an action", ("Preview Data", "Apply Red Flag Rules", "Generate SAR for Selected Transactions", "Search Customers with Multiple Violations"))

if uploaded_file is not None:
    transactions = load_data(uploaded_file)
    if transactions is not None:
        if option == "Preview Data":
            st.write("Uploaded Transaction Data")
            st.dataframe(transactions.head())
            # st.write("Transaction Velocity Distribution")
            # fig = px.histogram(transactions, x="velocity", title="Transaction Velocity Distribution")
            # st.plotly_chart(fig)

            # Visualizing Data Distribution
            st.write("Transaction Amount Distribution")
            fig = px.histogram(transactions, x="amount")
            st.plotly_chart(fig)

        elif option == "Apply Red Flag Rules":
            st.write("Uploaded Transaction Data")
            st.dataframe(transactions.head())

            red_flag_rules = [
                    'high_value_cash_deposits', 'structured_transactions', 'high_risk_country_transactions',
                     'high_velocity_cash_activity',
                    'keywords_hitting', 'unusual_transaction_patterns', 'large_incoming_wires'
                ]

            selected_rules = st.multiselect("Select Red Flag Rules to Apply", red_flag_rules)

            # Customer Selection (for filtering)
            selected_customer = st.selectbox("Select Customer (Optional)", ['All'] + transactions['customer_id'].unique().tolist(), index=0)

            if st.button("Apply Selected Red Flag Rules"):
                if selected_customer == 'All':
                    flagged_transactions = apply_red_flag_rules(transactions, selected_rules)
                else:
                    flagged_transactions = apply_red_flag_rules(transactions, selected_rules, customer_id=selected_customer)
                
                st.write("Flagged Transactions")
                for name in selected_rules:
                    if name in flagged_transactions and not flagged_transactions[name].empty:
                        with st.expander(f"Flagged Dataset: {name}"):
                            st.dataframe(flagged_transactions[name])
                            # Add visual summaries for each flagged dataset
                            st.write(f"Summary for {name}")
                            fig = px.histogram(flagged_transactions[name], x="amount")
                            st.plotly_chart(fig)

        elif option == "Generate SAR for Selected Transactions":
            red_flag_rules = [
                'high_value_cash_deposits', 'structured_transactions', 'high_risk_country_transactions',
                'rapid_movement_of_funds', 'inconsistent_business_activity', 'high_velocity_cash_activity',
                'third_party_transactions', 'unusual_transaction_patterns', 'commingling_of_funds', 'large_incoming_wires'
            ]

            flagged_transactions = apply_red_flag_rules(transactions, red_flag_rules)
            st.write("Flagged Transactions")
            flat_flagged_transactions = pd.concat(flagged_transactions.values()).drop_duplicates()
            st.dataframe(flat_flagged_transactions)

            selected_flags = st.multiselect("Select Transactions to Include in SAR", options=flat_flagged_transactions['transaction_id'], format_func=lambda x: f"Transaction ID: {x}")
            
            if selected_flags:
                selected_transactions = flat_flagged_transactions[flat_flagged_transactions['transaction_id'].isin(selected_flags)]
                st.write("Selected Transactions for SAR")
                st.dataframe(selected_transactions)
                
                st.write("Details of Broken Rules")
                for idx, row in selected_transactions.iterrows():
                    broken_rules = [name for name, dataset in flagged_transactions.items() if row['transaction_id'] in dataset['transaction_id'].values]
                    st.write(f"Transaction ID: {row['transaction_id']} broke the following rules: {', '.join(broken_rules)}")
                
                customer_id = selected_transactions.iloc[0]['customer_id']
                violations = [rule for rule in flagged_transactions if customer_id in flagged_transactions[rule]['customer_id'].values]
                
                if st.button("Generate SAR Narrative"):
                    sar_narrative = generate_sar_narrative(customer_id, violations, selected_transactions.to_dict('records'))
                    st.subheader("SAR Narrative")
                    st.text_area("Generated SAR Narrative", value=sar_narrative, height=700)

        elif option == "Search Customers with Multiple Violations":
            red_flag_rules = [
                'high_value_cash_deposits', 'structured_transactions', 'high_risk_country_transactions',
                'rapid_movement_of_funds', 'inconsistent_business_activity', 'high_velocity_cash_activity',
                'third_party_transactions', 'unusual_transaction_patterns', 'commingling_of_funds', 'large_incoming_wires'
            ]

            flagged_transactions = apply_red_flag_rules(transactions, red_flag_rules)
            customers_with_violations = get_customers_with_multiple_violations(flagged_transactions)

            # Filter customers by number of violations
            min_violations = st.number_input("Minimum Number of Violations", min_value=1, max_value=10, value=2)
            filtered_customers = {customer: rules for customer, rules in customers_with_violations.items() if len(rules) >= min_violations}

            # Pagination
            customers_per_page = st.number_input("Customers per Page", min_value=1, max_value=50, value=10)
            customer_ids = list(filtered_customers.keys())
            total_pages = (len(customer_ids) + customers_per_page - 1) // customers_per_page
            selected_page = st.selectbox("Select Page", range(1, total_pages + 1))

            start_index = (selected_page - 1) * customers_per_page
            end_index = start_index + customers_per_page
            paginated_customer_ids = customer_ids[start_index:end_index]

            # Create a dictionary to store SAR narratives for each customer
            if 'sar_narratives' not in st.session_state:
                st.session_state['sar_narratives'] = {}

            st.write("Customers with Multiple Rule Violations")
            for customer in paginated_customer_ids:
                rules = filtered_customers[customer]
                with st.expander(f"Customer ID: {customer}"):
                    st.write(f"Violated Rules: {', '.join(rules)}")
                    customer_transactions = transactions[transactions['customer_id'] == customer]
                    st.write(f"Transactions for Customer ID: {customer}")
                    st.dataframe(customer_transactions)

                    # Visualize transactions for each customer
                    st.write("Transaction Amount Distribution for Customer")
                    fig = px.histogram(customer_transactions, x="amount")
                    st.plotly_chart(fig)

                    rule_violations_count = {rule: sum(customer_transactions['transaction_id'].isin(flagged_transactions[rule]['transaction_id'])) for rule in rules}
                    st.write(f"Number of times each rule was broken for Customer ID: {customer}")
                    for rule, count in rule_violations_count.items():
                        st.write(f"{rule}: {count} times")

                    # Check if a narrative already exists for this customer
                    if customer in st.session_state['sar_narratives']:
                        st.subheader("SAR Narrative")
                        st.text_area("Generated SAR Narrative", value=st.session_state['sar_narratives'][customer], height=600)
                    else:
                        if st.button(f"Generate SAR Narrative for Customer {customer}"):
                            sar_narrative = generate_sar_narrative(customer, rules, customer_transactions.to_dict('records'))
                            st.session_state['sar_narratives'][customer] = sar_narrative  # Store the narrative in session state
                            st.experimental_rerun()  # Force re-run to display the narrative