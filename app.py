import streamlit as st
import joblib
import pandas as pd
from persona_config import PERSONA_DETAILS

# ------------------------------ FIX: Prevent hidden caching ------------------------------
st.cache_data.clear()

st.set_page_config(page_title="Customer Persona Predictor", layout="wide")


# ------------------------------ Load Model (cached once only) ------------------------------
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()


# ------------------------------ Feature Order ------------------------------
FEATURE_COLUMNS = [
    "Age", "Gender", "City_Tier", "Occupation", "Annual_Income", "AMB",
    "Debit_Txn_Count", "Credit_Txn_Count", "UPI_Usage_Ratio",
    "ATM_Withdrawal_Count", "Failed_Txn_Count", "Mobile_App_Login",
    "Netbanking_Login", "Dormancy_Days", "Products_Held",
    "Credit_Card_Utilization", "EMI_Presence", "Insurance_Premium",
    "SIP_Amount", "FD_Amount"
]


# ------------------------------ Feature Meta ------------------------------
FEATURE_META = {
    "Age": {"desc": "Customer age in years.", "reason": "Life-stage & financial needs."},
    "Gender": {"desc": "Self-identified gender.", "reason": "Used only for behaviour segmentation."},
    "City_Tier": {"desc": "City tier 1–3.", "reason": "Represents economic environment."},
    "Occupation": {"desc": "Occupation type.", "reason": "Income stability & behaviour."},
    "Annual_Income": {"desc": "Yearly income in ₹.", "reason": "Financial capacity."},
    "AMB": {"desc": "Avg Monthly Balance.", "reason": "Relationship depth."},
    "Debit_Txn_Count": {"desc": "Outgoing txns.", "reason": "Activity measure."},
    "Credit_Txn_Count": {"desc": "Incoming txns.", "reason": "Income/flows."},
    "UPI_Usage_Ratio": {"desc": "Digital UPI usage %.", "reason": "Digital adoption."},
    "ATM_Withdrawal_Count": {"desc": "ATM withdrawals.", "reason": "Cash dependency."},
    "Failed_Txn_Count": {"desc": "Failed transactions.", "reason": "Friction indicator."},
    "Mobile_App_Login": {"desc": "Mobile logins.", "reason": "Digital engagement."},
    "Netbanking_Login": {"desc": "Web logins.", "reason": "Digital maturity."},
    "Dormancy_Days": {"desc": "Inactive days.", "reason": "Churn risk."},
    "Products_Held": {"desc": "Products with bank.", "reason": "Cross-sell depth."},
    "Credit_Card_Utilization": {"desc": "Card usage %.", "reason": "Spending behaviour."},
    "EMI_Presence": {"desc": "Has active EMIs?", "reason": "Credit appetite."},
    "Insurance_Premium": {"desc": "Insurance spend.", "reason": "Protection maturity."},
    "SIP_Amount": {"desc": "Monthly SIP.", "reason": "Investment readiness."},
    "FD_Amount": {"desc": "FD value.", "reason": "Savings preference."},
}


def help_text(name):
    m = FEATURE_META.get(name, {})
    return f"{m.get('desc', '')}\n\n**Why important:** {m.get('reason', '')}"


# ==========================================================================================
#                                PERSONA CARDS (NEW SECTION)
# ==========================================================================================

st.title("🧠 Customer Persona Prediction App")

st.subheader("📌 The 4 Customer Personas in This Model")
st.write("Below is a quick overview of all personas before you enter customer details.")

persona_cols = st.columns(2)

for i, (cluster_id, details) in enumerate(PERSONA_DETAILS.items()):
    col = persona_cols[i % 2]
    with col:
        st.markdown(
            f"""
            <div style="
                border:2px solid #4CAF50;
                border-radius:12px;
                padding:15px;
                margin-bottom:15px;
                background:#F6FFF6;
            ">
                <h4 style="color:#2E7D32;">🧩 {details['name']}</h4>
                <p style="font-size:15px;">{details['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")


# ==========================================================================================
#                                INPUT FORM SECTION
# ==========================================================================================

with st.form("customer_form"):
    st.subheader("📋 Enter Customer Details")

    c1, c2, c3 = st.columns(3)

    with c1:
        Age = st.number_input("Age", 18, 100, 30, help=help_text("Age"))
        Gender = st.selectbox("Gender", ["Male", "Female", "Other"], help=help_text("Gender"))
        City_Tier = st.selectbox("City Tier", [1.0, 2.0, 3.0], help=help_text("City_Tier"))
        Occupation = st.selectbox("Occupation", ["Salaried", "Self-Employed", "Business Owner"], help=help_text("Occupation"))

    with c2:
        Annual_Income = st.number_input("Annual Income (₹)", 100000, 10000000, 800000, help=help_text("Annual_Income"))
        AMB = st.number_input("Average Monthly Balance (₹)", 0, 1000000, 50000, help=help_text("AMB"))
        Debit_Txn_Count = st.number_input("Debit Txn Count", 0, 300, 10, help=help_text("Debit_Txn_Count"))
        Credit_Txn_Count = st.number_input("Credit Txn Count", 0, 300, 5, help=help_text("Credit_Txn_Count"))

    with c3:
        UPI_Usage_Ratio = st.slider("UPI Usage Ratio", 0.0, 1.0, 0.5, help=help_text("UPI_Usage_Ratio"))
        ATM_Withdrawal_Count = st.number_input("ATM Withdrawals", 0, 50, 2, help=help_text("ATM_Withdrawal_Count"))
        Failed_Txn_Count = st.number_input("Failed Transactions", 0, 50, 1, help=help_text("Failed_Txn_Count"))
        Mobile_App_Login = st.number_input("Mobile App Logins", 0, 300, 20, help=help_text("Mobile_App_Login"))


    st.subheader("🔐 Banking Behaviour & Relationship")

    d1, d2, d3 = st.columns(3)

    with d1:
        Netbanking_Login = st.number_input("Netbanking Logins", 0, 300, 10, help=help_text("Netbanking_Login"))
        Dormancy_Days = st.number_input("Dormancy Days", 0, 365, 30, help=help_text("Dormancy_Days"))

    with d2:
        Products_Held = st.number_input("Products Held", 0, 10, 2, help=help_text("Products_Held"))
        Credit_Card_Utilization = st.number_input("Credit Card Utilization (%)", 0, 100, 40, help=help_text("Credit_Card_Utilization"))

    with d3:
        EMI_Presence = st.selectbox("EMI Presence", [0, 1], help=help_text("EMI_Presence"))
        Insurance_Premium = st.number_input("Insurance Premium", 0, 500000, 3000, help=help_text("Insurance_Premium"))
        SIP_Amount = st.number_input("SIP Amount", 0, 500000, 2000, help=help_text("SIP_Amount"))
        FD_Amount = st.number_input("FD Amount", 0, 10000000, 50000, help=help_text("FD_Amount"))

    submit = st.form_submit_button("🔍 Predict Persona")


# ==========================================================================================
#                                PREDICTION ENGINE
# ==========================================================================================

if submit:
    st.markdown("### ⏳ Generating Prediction...")

    input_df = pd.DataFrame([{
        "Age": Age, "Gender": Gender, "City_Tier": City_Tier, "Occupation": Occupation,
        "Annual_Income": Annual_Income, "AMB": AMB, "Debit_Txn_Count": Debit_Txn_Count,
        "Credit_Txn_Count": Credit_Txn_Count, "UPI_Usage_Ratio": UPI_Usage_Ratio,
        "ATM_Withdrawal_Count": ATM_Withdrawal_Count, "Failed_Txn_Count": Failed_Txn_Count,
        "Mobile_App_Login": Mobile_App_Login, "Netbanking_Login": Netbanking_Login,
        "Dormancy_Days": Dormancy_Days, "Products_Held": Products_Held,
        "Credit_Card_Utilization": Credit_Card_Utilization, "EMI_Presence": EMI_Presence,
        "Insurance_Premium": Insurance_Premium, "SIP_Amount": SIP_Amount, "FD_Amount": FD_Amount
    }], columns=FEATURE_COLUMNS)

    # Always compute prediction freshly
    with st.spinner("Predicting..."):
        prediction = model.predict(input_df)
        cluster_id = int(prediction[0])

    persona = PERSONA_DETAILS.get(cluster_id, {})

    st.success(f"### 🎯 Predicted Persona: **{persona.get('name', 'Unknown Persona')}**")
    st.write(f"**Description:** {persona.get('description', '')}")

    st.markdown("---")
    st.subheader("💡 Recommended Marketing Strategies")

    for rec in persona.get("recommendations", []):
        st.markdown(f"- ✅ {rec}")

