import streamlit as st
import joblib
import pandas as pd
from persona_config import PERSONA_DETAILS  # load persona names, descriptions, strategic recommendations

st.set_page_config(page_title="Customer Persona Predictor", layout="wide")

# ---------------- Load Trained Model ----------------
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# Feature order exactly as model expects
FEATURE_COLUMNS = [
    "Age", "Gender", "City_Tier", "Occupation", "Annual_Income", "AMB",
    "Debit_Txn_Count", "Credit_Txn_Count", "UPI_Usage_Ratio",
    "ATM_Withdrawal_Count", "Failed_Txn_Count", "Mobile_App_Login",
    "Netbanking_Login", "Dormancy_Days", "Products_Held",
    "Credit_Card_Utilization", "EMI_Presence", "Insurance_Premium",
    "SIP_Amount", "FD_Amount"
]


# ---------------- Feature meta: description + why it's used ----------------
FEATURE_META = {
    "Age": {
        "desc": "Customer age in years.",
        "reason": "Age is a proxy for life stage and financial product needs."
    },
    "Gender": {
        "desc": "Self-identified gender.",
        "reason": "Used only for behavior segmentation, not for pricing."
    },
    "City_Tier": {
        "desc": "Tier of city based on affluence (1=metro, 3=rural).",
        "reason": "Captures economic environment and product affinity."
    },
    "Occupation": {
        "desc": "Customer's primary occupation.",
        "reason": "Impacts income stability & spending behavior."
    },
    "Annual_Income": {
        "desc": "Approximate annual income in ₹.",
        "reason": "Key predictor of financial product appetite."
    },
    "AMB": {
        "desc": "Average monthly balance maintained.",
        "reason": "Reflects commitment to banking relationship."
    },
    "Debit_Txn_Count": {
        "desc": "Monthly outgoing debit transaction count.",
        "reason": "Shows account activity level."
    },
    "Credit_Txn_Count": {
        "desc": "Monthly incoming credit transaction count.",
        "reason": "Useful for salary & inflow patterns."
    },
    "UPI_Usage_Ratio": {
        "desc": "Digital adoption via UPI payments.",
        "reason": "Indicates affinity for digital financial products."
    },
    "ATM_Withdrawal_Count": {
        "desc": "Cash withdrawal frequency.",
        "reason": "Shows cash dependency vs digital maturity."
    },
    "Failed_Txn_Count": {
        "desc": "Failures faced in a month.",
        "reason": "Possible friction → cross-sell risk mitigation."
    },
    "Mobile_App_Login": {
        "desc": "Number of mobile app logins per month.",
        "reason": "Digital behaviour classifier."
    },
    "Netbanking_Login": {
        "desc": "Web-based banking logins per month.",
        "reason": "Indicates digital involvement & engagement."
    },
    "Dormancy_Days": {
        "desc": "Days since customer last used the bank actively.",
        "reason": "Critical for early churn prediction."
    },
    "Products_Held": {
        "desc": "Number of bank products customer holds.",
        "reason": "Relationship depth indicator."
    },
    "Credit_Card_Utilization": {
        "desc": "Credit card usage percentage.",
        "reason": "Spending pattern & credit appetite."
    },
    "EMI_Presence": {
        "desc": "If customer has active EMIs.",
        "reason": "Shows credit penetration & cash flow stress."
    },
    "Insurance_Premium": {
        "desc": "Insurance spending.",
        "reason": "Protection product maturity & appetite."
    },
    "SIP_Amount": {
        "desc": "Monthly SIP.",
        "reason": "Investment maturity."
    },
    "FD_Amount": {
        "desc": "Total FD holdings.",
        "reason": "Conservative saving behaviour."
    },
}


def help_text(feature_name: str):
    meta = FEATURE_META.get(feature_name, {})
    return f"{meta.get('desc', '')}\n\n**Reason:** {meta.get('reason', '')}"


# ------------------------ HEADER ------------------------
st.title("🧠 Customer Persona Prediction App")
st.write("Enter the customer details below to get predicted persona + marketing recommendations.")

st.markdown("---")

# ------------------------ INPUT FORM ------------------------
with st.form("customer_form"):
    st.subheader("📋 Enter Customer Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        Age = st.number_input("Age", 18, 100, 30, help=help_text("Age"))
        Gender = st.selectbox("Gender", ["Male", "Female", "Other"], help=help_text("Gender"))
        City_Tier = st.selectbox("City Tier", [1.0, 2.0, 3.0], help=help_text("City_Tier"))
        Occupation = st.selectbox("Occupation", ["Salaried", "Self-Employed", "Business Owner"], help=help_text("Occupation"))

    with col2:
        Annual_Income = st.number_input("Annual Income (₹)", 100000, 10000000, 800000, help=help_text("Annual_Income"))
        AMB = st.number_input("Average Monthly Balance (₹)", 0, 1000000, 50000, help=help_text("AMB"))
        Debit_Txn_Count = st.number_input("Debit Txn Count", 0, 300, 10, help=help_text("Debit_Txn_Count"))
        Credit_Txn_Count = st.number_input("Credit Txn Count", 0, 300, 5, help=help_text("Credit_Txn_Count"))

    with col3:
        UPI_Usage_Ratio = st.slider("UPI Usage Ratio", 0.0, 1.0, 0.5, help=help_text("UPI_Usage_Ratio"))
        ATM_Withdrawal_Count = st.number_input("ATM Withdrawals", 0, 50, 2, help=help_text("ATM_Withdrawal_Count"))
        Failed_Txn_Count = st.number_input("Failed Transactions", 0, 50, 1, help=help_text("Failed_Txn_Count"))
        Mobile_App_Login = st.number_input("Mobile App Logins", 0, 300, 20, help=help_text("Mobile_App_Login"))

    st.markdown("### 🔐 Banking Behaviour & Relationship")

    col4, col5, col6 = st.columns(3)

    with col4:
        Netbanking_Login = st.number_input("Netbanking Logins", 0, 300, 10, help=help_text("Netbanking_Login"))
        Dormancy_Days = st.number_input("Dormancy Days", 0, 365, 30, help=help_text("Dormancy_Days"))

    with col5:
        Products_Held = st.number_input("Products Held", 0, 10, 2, help=help_text("Products_Held"))
        Credit_Card_Utilization = st.number_input("Credit Card Utilization (%)", 0, 100, 40, help=help_text("Credit_Card_Utilization"))

    with col6:
        EMI_Presence = st.selectbox("EMI Presence", [0, 1], help=help_text("EMI_Presence"))
        Insurance_Premium = st.number_input("Insurance Premium", 0, 500000, 3000, help=help_text("Insurance_Premium"))
        SIP_Amount = st.number_input("SIP Amount", 0, 500000, 2000, help=help_text("SIP_Amount"))
        FD_Amount = st.number_input("FD Amount", 0, 10000000, 50000, help=help_text("FD_Amount"))

    submit = st.form_submit_button("🔍 Predict Persona")

# ------------------------ PREDICTION LOGIC ------------------------
if submit:
    st.markdown("### ⏳ Generating Prediction...")

    # Prepare input in correct format
    input_data = pd.DataFrame([{
        "Age": Age,
        "Gender": Gender,
        "City_Tier": City_Tier,
        "Occupation": Occupation,
        "Annual_Income": Annual_Income,
        "AMB": AMB,
        "Debit_Txn_Count": Debit_Txn_Count,
        "Credit_Txn_Count": Credit_Txn_Count,
        "UPI_Usage_Ratio": UPI_Usage_Ratio,
        "ATM_Withdrawal_Count": ATM_Withdrawal_Count,
        "Failed_Txn_Count": Failed_Txn_Count,
        "Mobile_App_Login": Mobile_App_Login,
        "Netbanking_Login": Netbanking_Login,
        "Dormancy_Days": Dormancy_Days,
        "Products_Held": Products_Held,
        "Credit_Card_Utilization": Credit_Card_Utilization,
        "EMI_Presence": EMI_Presence,
        "Insurance_Premium": Insurance_Premium,
        "SIP_Amount": SIP_Amount,
        "FD_Amount": FD_Amount,
    }], columns=FEATURE_COLUMNS)

    # Model prediction
    cluster_id = int(model.predict(input_data)[0])
    persona = PERSONA_DETAILS.get(cluster_id, {})

    # ---------------- Display results ----------------
    st.success(f"### 🎯 Predicted Persona: **{persona.get('name', 'Unknown Persona')}**")
    st.write(f"**Description:** {persona.get('description', '')}")

    st.markdown("---")
    st.subheader("💡 Recommended Marketing Strategies")

    for rec in persona.get("recommendations", []):
        st.markdown(f"- ✅ {rec}")
