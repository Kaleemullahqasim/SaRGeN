import pandas as pd

# Load high-risk countries from CSV file
def load_high_risk_countries(file_path='data/high_risk_countries.csv'):
    try:
        high_risk_countries_df = pd.read_csv(file_path)
        high_risk_countries = high_risk_countries_df['Name'].tolist()
        return high_risk_countries
    except Exception as e:
        print(f"Error loading high-risk countries: {e}")
        return []

high_risk_countries = load_high_risk_countries()

# Load keywords from CSV file
def load_keywords(file_path='data/high_risk_keywords.csv'):
    try:
        keywords_df = pd.read_csv(file_path)
        keywords = keywords_df['Keyword'].astype(str).tolist()
        return keywords
    except Exception as e:
        print(f"Error loading keywords: {e}")
        return []
keywords = load_keywords()


def detect_high_risk_country_transactions(transactions):
    return transactions[transactions['country'].isin(high_risk_countries)]

def detect_keywords_hitting(transactions):
    pattern = '|'.join(keywords)
    return transactions[transactions['description'].str.contains(pattern, case=False)]


def detect_high_value_cash_deposits(transactions):
    return transactions[(transactions['transaction_type'] == 'deposit') & (transactions['amount'] > 9000)]

def detect_structured_transactions(transactions):
    return transactions[(transactions['amount'] < 10000) & (transactions['amount'] > 9000)]

# def detect_rapid_movement_of_funds(transactions):
#     return transactions[transactions['velocity'] > 7]

def detect_inconsistent_business_activity(transactions):
    return transactions[transactions['account_balance'] < transactions['amount']]

def detect_high_velocity_cash_activity(transactions):
    return transactions[transactions['velocity'] > 8]

# def detect_third_party_transactions(transactions):
#     return transactions[transactions['description'].str.contains("third party", case=False)]

def detect_unusual_transaction_patterns(transactions):
    return transactions[(transactions['amount'] > 5000) & (transactions['transaction_type'] == 'withdrawal') & (transactions['velocity'] > 5)]

def detect_large_incoming_wires(transactions):
    high_risk_countries = load_high_risk_countries()  # Re-load in case of changes during runtime
    return transactions[(transactions['amount'] > 15000) & (transactions['transaction_type'] == 'transfer') & (transactions['country'].isin(high_risk_countries))]
