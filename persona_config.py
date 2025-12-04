# persona_config.py

# ------------- PERSONA DEFINITIONS (by cluster id) -----------------

PERSONA_DETAILS = {
    0: {
        "name": "Young Digital Transactors",
        "description": (
            "Young, mid-income customers who are heavy UPI users and "
            "transact frequently through digital channels."
        ),
        "recommendations": [
            "Offer a starter / entry-level credit card with UPI-linked rewards.",
            "Promote small SIP starter packs (₹2k–₹3k) and goal-based investing.",
            "Run app-based cashback / gamified engagement campaigns."
        ],
    },
    1: {
        "name": "Affluent Offline Savers",
        "description": (
            "Older, high-balance customers with large FDs who prefer assisted "
            "or offline banking and use digital channels less frequently."
        ),
        "recommendations": [
            "Offer RM-led wealth management and FD-to-mutual-fund migration.",
            "Bundle senior-focused life & health insurance products.",
            "Provide assisted digital onboarding and priority customer service."
        ],
    },
    2: {
        "name": "Urban Affluent Digital Power Users",
        "description": (
            "High-income, mostly Tier-1 customers with strong card usage, "
            "high SIP contribution and very high mobile app activity."
        ),
        "recommendations": [
            "Cross-sell premium credit cards with travel and lifestyle benefits.",
            "Promote equity SIPs, PMS/wealth products and advanced investing tools.",
            "Offer pre-approved high-value personal loans / BNPL lines."
        ],
    },
    3: {
        "name": "Semi-Urban Cash-Heavy Aspirers",
        "description": (
            "Mid-income, Tier-2/3 customers who rely heavily on ATM and debit, "
            "with moderate digital adoption and growing savings."
        ),
        "recommendations": [
            "Promote debit-card reward programs and ATM fee waivers.",
            "Push UPI adoption and simple digital journeys for everyday payments.",
            "Offer small-ticket personal loans and financial literacy campaigns."
        ],
    },
}

# ------------- FEATURE METADATA (name, description, reason, widget) -----------------

# NOTE: order here MUST match the training column order
FEATURE_META = {
    "Age": {
        "label": "Age",
        "description": "Customer age in years.",
        "why": "Age correlates with life stage, income stability and product needs.",
        "widget": "number",
    },
    "Gender": {
        "label": "Gender",
        "description": "Customer gender (Male / Female / Other).",
        "why": "Used as a demographic variable to analyse behaviour across segments.",
        "widget": "select",
        "options": ["Male", "Female", "Other"],
    },
    "City_Tier": {
        "label": "City Tier",
        "description": "1 = Metro, 2 = Tier-2, 3 = Tier-3 / semi-urban.",
        "why": "City tier captures access to infrastructure, income levels and channel mix.",
        "widget": "select",
        "options": [1.0, 2.0, 3.0],
    },
    "Occupation": {
        "label": "Occupation",
        "description": "Primary occupation of the customer.",
        "why": "Income stability and risk appetite differ by occupation type.",
        "widget": "select",
        "options": ["Salaried", "Self-Employed", "Business Owner"],
    },
    "Annual_Income": {
        "label": "Annual Income",
        "description": "Estimated annual income (₹).",
        "why": "Higher income typically enables higher spends and investment capacity.",
        "widget": "number",
    },
    "AMB": {
        "label": "Average Monthly Balance (AMB)",
        "description": "Average balance maintained in the account per month (₹).",
        "why": "Indicates savings power and depth of relationship.",
        "widget": "number",
    },
    "Debit_Txn_Count": {
        "label": "Debit Transaction Count",
        "description": "Number of debit-card / account debit transactions per month.",
        "why": "Shows frequency of account usage for everyday payments.",
        "widget": "number",
    },
    "Credit_Txn_Count": {
        "label": "Credit Transaction Count",
        "description": "Number of credit-card transactions per month.",
        "why": "Captures credit adoption and repayment behaviour.",
        "widget": "number",
    },
    "UPI_Usage_Ratio": {
        "label": "UPI Usage Ratio",
        "description": "Share of transactions done through UPI (0–1).",
        "why": "Shows how digitally active the customer is in day-to-day spends.",
        "widget": "number",
    },
    "ATM_Withdrawal_Count": {
        "label": "ATM Withdrawal Count",
        "description": "Number of ATM cash withdrawals per month.",
        "why": "High counts indicate cash dependency instead of digital.",
        "widget": "number",
    },
    "Failed_Txn_Count": {
        "label": "Failed Transaction Count",
        "description": "Number of failed transactions per month.",
        "why": "Signals friction in digital usage or risk of churn due to poor experience.",
        "widget": "number",
    },
    "Mobile_App_Login": {
        "label": "Mobile App Logins",
        "description": "Number of mobile banking app logins per month.",
        "why": "Strong proxy for digital engagement with the bank.",
        "widget": "number",
    },
    "Netbanking_Login": {
        "label": "Netbanking Logins",
        "description": "Number of internet banking logins per month.",
        "why": "Captures web-channel engagement and transaction planning.",
        "widget": "number",
    },
    "Dormancy_Days": {
        "label": "Dormancy Days",
        "description": "Days since last core account activity.",
        "why": "Higher values indicate disengagement and potential churn risk.",
        "widget": "number",
    },
    "Products_Held": {
        "label": "Products Held",
        "description": "Number of bank products held (CASA, card, loan, etc.).",
        "why": "Measures depth of relationship and cross-holding.",
        "widget": "number",
    },
    "Credit_Card_Utilization": {
        "label": "Credit Card Utilization (%)",
        "description": "Average utilization of credit limit (0–100%).",
        "why": "Captures credit behaviour and potential for upsell.",
        "widget": "number",
    },
    "EMI_Presence": {
        "label": "EMI Presence",
        "description": "Whether customer has any active EMI (0 = No, 1 = Yes).",
        "why": "Indicates existing credit exposure and propensity for further loans.",
        "widget": "select",
        "options": [0, 1],
    },
    "Insurance_Premium": {
        "label": "Monthly Insurance Premium",
        "description": "Total monthly insurance premium paid (₹).",
        "why": "Shows protection mindset and ability to invest in risk cover.",
        "widget": "number",
    },
    "SIP_Amount": {
        "label": "Monthly SIP Amount",
        "description": "Total monthly SIP contribution (₹).",
        "why": "Strong signal of investment maturity and wealth-building behaviour.",
        "widget": "number",
    },
    "FD_Amount": {
        "label": "Total FD Amount",
        "description": "Current outstanding FD principal (₹).",
        "why": "Indicates conservative savings and long-term deposit behaviour.",
        "widget": "number",
    },
}
