import streamlit as st
# Set page config first
st.set_page_config(page_title="BSA / AML Detection System", layout="wide")

# Rest of the imports
import pandas as pd
import numpy as np
import plotly.express as px
import logging
from sar_groq import generate_sar_narrative
from red_flag_rules import (detect_high_value_cash_deposits, detect_structured_transactions,
                            detect_high_risk_country_transactions, 
                            detect_high_velocity_cash_activity,
                            detect_keywords_hitting, detect_unusual_transaction_patterns,
                            detect_large_incoming_wires)
from modules.visualization import (create_transaction_amount_distribution,
                                 create_violations_summary,
                                 create_customer_dashboard,
                                 create_preview_dashboard,
                                 create_summary_metrics,
                                 VisualizationTheme)  # Add VisualizationTheme to imports
from modules.data_processing import TransactionProcessor

# Apply unified styling at the start
st.markdown(VisualizationTheme.get_css(), unsafe_allow_html=True)

# Define red flag rules
red_flag_rules = [
    'high_value_cash_deposits',
    'structured_transactions',
    'high_risk_country_transactions',
    'high_velocity_cash_activity',
    'keywords_hitting',
    'unusual_transaction_patterns',
    'large_incoming_wires'
]

# Helper Functions
def format_sar_narrative(narrative):
    """Format SAR narrative in a structured way"""
    sections = [
        "SUMMARY OF SUSPICIOUS ACTIVITY",
        "CUSTOMER DETAILS",
        "TRANSACTION PATTERNS",
        "RED FLAGS IDENTIFIED",
        "CONCLUSION"
    ]
    
    formatted_text = ""
    current_section = ""
    
    for line in narrative.split('\n'):
        for section in sections:
            if section.lower() in line.lower():
                current_section = section
                formatted_text += f"\n\n{section}\n{'='*len(section)}\n"
                break
        else:
            if line.strip():
                formatted_text += line + "\n"
    
    return formatted_text

def display_sar_narrative(narrative, customer_id):
    """Display formatted SAR narrative with unique key per customer"""
    formatted_narrative = format_sar_narrative(narrative)
    st.markdown("### Suspicious Activity Report (SAR) Narrative")
    st.markdown(VisualizationTheme.get_styled_text_area(), unsafe_allow_html=True)
    st.text_area(
        "",
        value=formatted_narrative,
        height=700,
        key=f"sar_narrative_{customer_id}"  # Make key unique for each customer
    )

def create_flagged_transaction_visual(data, title):
    """Create consistent visualization for flagged transactions"""
    fig = px.histogram(
        data,
        x="amount",
        title=title,
        nbins=30,
        opacity=0.75,
        color_discrete_sequence=[VisualizationTheme.COLORS['warning']]
    )
    fig.update_layout(
        bargap=0.2,
        xaxis_title="Transaction Amount",
        yaxis_title="Frequency"
    )
    return VisualizationTheme.apply_theme(fig)

# Update the CSS application
def apply_custom_css():
    st.markdown(f"""
        <style>
        .main {{ 
            padding: 0rem 1rem;
            background-color: {VisualizationTheme.COLORS['background']};
            color: {VisualizationTheme.COLORS['text']};
        }}
        .stButton>button {{ 
            width: 100%;
            background-color: {VisualizationTheme.COLORS['primary']};
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            border: none;
            font-weight: 500;
        }}
        .stSelectbox [data-baseweb="select"] {{
            background-color: {VisualizationTheme.COLORS['background']};
        }}
        .stMultiSelect [data-baseweb="select"] {{
            background-color: {VisualizationTheme.COLORS['background']};
        }}
        .css-1d391kg {{ background-color: {VisualizationTheme.COLORS['background']} }}
        .stMetric {{ 
            background-color: rgba(27,38,59,0.5);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border: 1px solid {VisualizationTheme.COLORS['grid']};
        }}
        .element-container {{ margin: 1rem 0; }}
        .stDataFrame {{ 
            background-color: {VisualizationTheme.COLORS['background']};
            border-radius: 5px;
            padding: 1rem;
        }}
        .stTextArea textarea {{
            background-color: {VisualizationTheme.COLORS['background']};
            color: {VisualizationTheme.COLORS['text']};
            font-family: 'Arial', sans-serif;
            font-size: 14px;
            line-height: 1.5;
            padding: 15px;
            border: 1px solid {VisualizationTheme.COLORS['grid']};
            border-radius: 5px;
        }}
        </style>
    """, unsafe_allow_html=True)

def create_section_header(title):
    """Creates consistently styled section headers"""
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

def create_metric_card(title, value):
    """Creates consistently styled metric cards"""
    return f"""
        <div class="stMetric">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
    """

# Apply CSS at the start
apply_custom_css()

# Initialize session state
if 'processor' not in st.session_state:
    st.session_state.processor = TransactionProcessor()
if 'sar_narratives' not in st.session_state:
    st.session_state.sar_narratives = {}


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

# Function to generate and display SAR narrative
def generate_and_display_sar(customer, rules):
    customer_transactions = transactions[transactions['customer_id'] == customer]
    try:
        sar_narrative = generate_sar_narrative(customer, rules, customer_transactions.to_dict('records'))
        st.session_state['sar_narratives'][customer] = sar_narrative
        display_sar_narrative(sar_narrative, customer)  # Pass customer ID
    except Exception as e:
        logging.error(f"Error generating SAR narrative: {e}")  # Log the error
        st.error(f"An error occurred while generating the SAR narrative. Please check the logs for details.")

# Streamlit App
st.title("Bank Secrecy Act (BSA) / Anti-Money Laundering (AML) Detection System")

# Sidebar for file upload and options
with st.sidebar:
    st.header("Upload and Options")
    uploaded_file = st.file_uploader("Upload Transaction Data (CSV)", type=["csv"])
    option = st.selectbox("Choose an action", ("Preview Data", "Apply Red Flag Rules", "Generate SAR for Selected Transactions", "Search Customers with Multiple Violations"))

if uploaded_file is not None:
    transactions = load_data(uploaded_file)
    if transactions is not None:
        if option == "Preview Data":
            create_section_header("Transaction Overview")
            
            # Create and display metrics with improved spacing
            metrics = create_summary_metrics(transactions)
            metric_cols = st.columns(len(metrics))
            for col, (_, metric) in zip(metric_cols, metrics.items()):
                with col:
                    st.markdown(
                        f"""
                        <div style='{metric["style"]}'>
                            <h4 style='margin:0;color:#90E0EF'>{metric["title"]}</h4>
                            <h2 style='margin:0.5rem 0;color:#E0E1DD'>{metric["value"]}</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create and display visualizations with interaction config
            volume_fig, amount_fig, types_fig = create_preview_dashboard(transactions)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(
                    volume_fig,
                    use_container_width=True,
                    config=VisualizationTheme.INTERACTION_CONFIG
                )
                st.plotly_chart(
                    types_fig,
                    use_container_width=True,
                    config=VisualizationTheme.INTERACTION_CONFIG
                )
            
            with col2:
                st.plotly_chart(
                    amount_fig,
                    use_container_width=True,
                    config=VisualizationTheme.INTERACTION_CONFIG
                )
                with st.expander("Transaction Statistics"):
                    st.markdown("""
                        <style>
                        .dataframe {
                            background-color: rgba(27,38,59,0.5);
                            color: #E0E1DD;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    st.table(transactions.describe()[['amount']].round(2))

        elif option == "Apply Red Flag Rules":
            create_section_header("Red Flag Analysis")
            
            with st.expander("View Transaction Data"):
                st.dataframe(transactions.head())

            col1, col2 = st.columns([2, 1])
            with col1:
                selected_rules = st.multiselect(
                    "Select Red Flag Rules to Apply",
                    red_flag_rules,  # Now using the defined list
                    help="Choose one or more rules to analyze transactions"
                )
            
            with col2:
                selected_customer = st.selectbox(
                    "Filter by Customer (Optional)",
                    ['All'] + sorted(transactions['customer_id'].unique().tolist()),
                    index=0
                )

            if st.button("Apply Selected Red Flag Rules"):
                if selected_rules:  # Changed from if/return to if/else
                    flagged_transactions = apply_red_flag_rules(
                        transactions, 
                        selected_rules, 
                        customer_id=None if selected_customer == 'All' else selected_customer
                    )
                    
                    st.markdown("### Flagged Transactions Analysis")
                    for name in selected_rules:
                        if name in flagged_transactions and not flagged_transactions[name].empty:
                            with st.expander(f"🚩 {name.replace('_', ' ').title()}", expanded=True):
                                col1, col2 = st.columns([2, 1])
                                with col1:
                                    st.dataframe(flagged_transactions[name])
                                with col2:
                                    fig = create_flagged_transaction_visual(
                                        flagged_transactions[name],
                                        f"Distribution for {name.replace('_', ' ').title()}"
                                    )
                                    st.plotly_chart(
                                        fig, 
                                        use_container_width=True,
                                        config=VisualizationTheme.INTERACTION_CONFIG
                                    )
                else:
                    st.warning("Please select at least one rule to apply")

        elif option == "Generate SAR for Selected Transactions":
            create_section_header("SAR Generation")
            # Use the same red_flag_rules list defined at top
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
                    display_sar_narrative(sar_narrative, customer_id)  # Pass customer ID

        elif option == "Search Customers with Multiple Violations":
            create_section_header("Customer Violation Analysis")
            
            flagged_transactions = apply_red_flag_rules(transactions, red_flag_rules)
            customers_with_violations = get_customers_with_multiple_violations(flagged_transactions)

            # Controls in columns
            col1, col2 = st.columns([1, 1])
            with col1:
                min_violations = st.number_input(
                    "Minimum Number of Violations",
                    min_value=1,
                    max_value=10,
                    value=2,
                    help="Filter customers by minimum number of rule violations"
                )
            with col2:
                customers_per_page = st.number_input(
                    "Customers per Page",
                    min_value=1,
                    max_value=50,
                    value=10
                )

            filtered_customers = {customer: rules for customer, rules in customers_with_violations.items() 
                               if len(rules) >= min_violations}

            # Pagination controls
            total_pages = (len(filtered_customers) + customers_per_page - 1) // customers_per_page
            if total_pages > 0:
                selected_page = st.selectbox(
                    "Page",
                    range(1, total_pages + 1),
                    format_func=lambda x: f"Page {x} of {total_pages}"
                )
                
                start_index = (selected_page - 1) * customers_per_page
                end_index = start_index + customers_per_page
                paginated_customer_ids = list(filtered_customers.keys())[start_index:end_index]

                st.markdown("### Customers with Multiple Rule Violations")
                
                for customer in paginated_customer_ids:
                    rules = filtered_customers[customer]
                    with st.expander(f"🔍 Customer ID: {customer}", expanded=True):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            # Customer transaction summary
                            customer_transactions = transactions[transactions['customer_id'] == customer]
                            metrics = create_summary_metrics(customer_transactions)
                            metric_cols = st.columns(len(metrics))
                            for mcol, (_, metric) in zip(metric_cols, metrics.items()):
                                with mcol:
                                    st.markdown(
                                        f"""
                                        <div style='{metric["style"]}'>
                                            <h4 style='margin:0;color:#90E0EF'>{metric["title"]}</h4>
                                            <h2 style='margin:0.5rem 0;color:#E0E1DD'>{metric["value"]}</h2>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                            
                            st.markdown("#### Transaction Data")
                            st.dataframe(customer_transactions, height=200)
                        
                        with col2:
                            # Violations summary
                            st.markdown("#### Rule Violations")
                            rule_violations_count = {
                                rule: sum(customer_transactions['transaction_id'].isin(
                                    flagged_transactions[rule]['transaction_id']
                                )) for rule in rules
                            }
                            violations_fig = create_violations_summary(rule_violations_count)
                            st.plotly_chart(
                                violations_fig,
                                use_container_width=True,
                                config=VisualizationTheme.INTERACTION_CONFIG
                            )
                        
                        # Transaction distribution
                        st.markdown("#### Transaction Analysis")
                        volume_fig, amount_fig, types_fig = create_preview_dashboard(customer_transactions)
                        subcol1, subcol2 = st.columns(2)
                        with subcol1:
                            st.plotly_chart(
                                volume_fig,
                                use_container_width=True,
                                config=VisualizationTheme.INTERACTION_CONFIG
                            )
                        with subcol2:
                            st.plotly_chart(
                                amount_fig,
                                use_container_width=True,
                                config=VisualizationTheme.INTERACTION_CONFIG
                            )

                        # SAR Generation
                        if st.button(f"Generate SAR Narrative for Customer {customer}"):
                            generate_and_display_sar(customer, rules)

                        if customer in st.session_state['sar_narratives']:
                            display_sar_narrative(st.session_state['sar_narratives'][customer], customer)  # Pass customer ID
            else:
                st.warning("No customers found with the specified number of violations.")