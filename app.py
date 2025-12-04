import streamlit as st
import joblib
import pandas as pd
from persona_config import PERSONA_DETAILS

st.set_page_config(page_title="Customer Persona Predictor", layout="wide")


# ---------------------------------------------------------
# LOAD MODEL ONLY ONCE
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()


# ---------------------------------------------------------
# FEATURE ORDER (MUST MATCH PIPELINE)
# ---------------------------------------------------------
FEATURE_COLUMNS = [
    "Age", "Gender", "City_Tier", "Occupation", "Annual_Income", "AMB",
    "Debit_Txn_Count", "Credit_Txn_Count", "UPI_Usage_Ratio",
    "ATM_Withdrawal_Count", "Failed_Txn_Count", "Mobile_App_Login",
    "Netbanking_Login", "Dormancy_Days", "Products_Held",
    "Credit_Card_Utilization", "EMI_Presence", "Insurance_Premium",
    "SIP_Amount", "FD_Amount"
]


# ---------------------------------------------------------
# PERSONA CARDS AT THE TOP (Option A)
# ---------------------------------------------------------
st.title("🧠 Customer Persona Prediction App")

st.markdown("### 📌 Four Customer Personas Identified in the Dataset")
persona_container = st.container()

with persona_container:
    cols = st.columns(2)

    persona_items = list(PERSONA_DETAILS.items())

    for idx, (pid, pdata) in enumerate(persona_items):
        col = cols[idx % 2]
        with col:
            st.markdown(
                f"""
                <div style="
                    background-color:#f5f5f5;
                    padding:18px;
                    border-radius:10px;
                    margin-bottom:20px;
                    border-left:6px solid #4CAF50;">
                    <h4>🧩 Persona {pid}: {pdata['name']}</h4>
                    <p><b>Description:</b> {pdata['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

st.markdown("---")


# ---------------------------------------------------------
# FEATURE META HELP TEXT
# ---------------------------------------------------------
FEATURE_META = {
    "Age": {"desc": "Customer age in years.",
            "reason": "Age influences life stage & financial needs."},
    "Gender": {"desc": "Customer gender.", 
               "reason": "Used only for segmentation, not pricing."},
    "City_Tier": {"desc": "Tier 1/2/3 city.",
                  "reason": "Captures economic environment."},
    "Occupation": {"desc": "Customer's primary occupation.",
                   "reason": "Influences income stability & product use."},
    "Annual_Income": {"desc": "Yearly income in ₹.",
                      "reason": "Strong predictor of product appetite."},
    "AMB": {"desc": "Average monthly balance.",
            "reason": "Relationship & engagement indicator."},
    "Debit_Txn_Count": {"desc": "Monthly debit transactions.",
                        "reason": "Shows spending activity."},
    "Credit_Txn_Count": {"desc": "Monthly credit transactions.",
                         "reason": "Shows salary / inflow patterns."},
    "UPI_Usage_Ratio": {"desc": "Digital UPI usage.",
                        "reason": "Indicates digital adoption."},
    "ATM_Withdrawal_Count": {"desc": "ATM withdrawals per month.",
                             "reason": "Shows cash dependency."},
    "Failed_Txn_Count": {"desc": "Failed transactions.",
                         "reason": "Indicates friction."},
    "Mobile_App_Login": {"desc": "App logins per month.",
                         "reason": "Digital adoption signal."},
    "Netbanking_Login": {"desc": "Web logins.",
                         "reason": "Another digital usage indicator."},
    "Dormancy_Days": {"desc": "Days since last active use.",
                      "reason": "Critical for engagement risk."},
    "Products_Held": {"desc": "Number of banking products.",
                      "reason": "Relationship depth."},
    "Credit_Card_Utilization": {"desc": "CC utilization percentage.",
                                "reason": "Credit appetite."},
    "EMI_Presence": {"desc": "Whether user has active EMIs.",
                     "reason": "Shows credit penetration."},
    "Insurance_Premium": {"desc": "Insurance premium paid.",
                          "reason": "Protection appetite."},
    "SIP_Amount": {"desc": "Monthly SIP amount.",
                   "reason": "Investment maturity."},
    "FD_Amount": {"desc": "Fixed deposits.",
                  "reason": "Conservative savings indicator."},
}


def help_text(feature):
    meta = FEATURE_META.get(feature, {})
    return f"{meta.get('desc','')}\n\nReason: {meta.get('reason','')}"


# ---------------------------------------------------------
# INPUT FORM — RERUN SAFE
# ---------------------------------------------------------
st.header("📋 Enter Customer Details Below")
st.write("Fill the form and click **Predict Persona**.")

with st.form("customer_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        Age = st.number_input("Age", 18, 100, 30, help=help_text("Age"))
        Gender = st.selectbox("Gender", ["Male", "Female", "Other"], help=help_text("Gender"))
        City_Tier = st.selectbox("City Tier", [1.0, 2.0, 3.0], help=help_text("City_Tier"))
        Occupation = st.selectbox("Occupation", ["Salaried", "Self-Employed", "Business Owner"], help=help_text("Occupation"))

    with col2:
        Annual_Income = st.number_input("Annual Income (₹)", 100000, 30000000, 800000, help=help_text("Annual_Income"))
        AMB = st.number_input("Average Monthly Balance", 0, 2000000, 50000, help=help_text("AMB"))
        Debit_Txn_Count = st.number_input("Debit Txns", 0, 300, 10, help=help_text("Debit_Txn_Count"))
        Credit_Txn_Count = st.number_input("Credit Txns", 0, 300, 5, help=help_text("Credit_Txn_Count"))

    with col3:
        UPI_Usage_Ratio = st.slider("UPI Usage Ratio", 0.0, 1.0, 0.4, help=help_text("UPI_Usage_Ratio"))
        ATM_Withdrawal_Count = st.number_input("ATM Withdrawals", 0, 50, 2, help=help_text("ATM_Withdrawal_Count"))
        Failed_Txn_Count = st.number_input("Failed Txns", 0, 20, 1, help=help_text("Failed_Txn_Count"))
        Mobile_App_Login = st.number_input("Mobile App Logins", 0, 500, 20, help=help_text("Mobile_App_Login"))

    col4, col5, col6 = st.columns(3)

    with col4:
        Netbanking_Login = st.number_input("Netbanking Logins", 0, 500, 10, help=help_text("Netbanking_Login"))
        Dormancy_Days = st.number_input("Dormancy Days", 0, 365, 30, help=help_text("Dormancy_Days"))

    with col5:
        Products_Held = st.number_input("Products Held", 0, 10, 2, help=help_text("Products_Held"))
        Credit_Card_Utilization = st.number_input("CC Utilization (%)", 0, 100, 40, help=help_text("Credit_Card_Utilization"))

    with col6:
        EMI_Presence = st.selectbox("EMI Presence", [0, 1], help=help_text("EMI_Presence"))
        Insurance_Premium = st.number_input("Insurance Premium", 0, 200000, 3000, help=help_text("Insurance_Premium"))
        SIP_Amount = st.number_input("SIP Amount", 0, 500000, 2000, help=help_text("SIP_Amount"))
        FD_Amount = st.number_input("FD Amount", 0, 50000000, 50000, help=help_text("FD_Amount"))

    submit = st.form_submit_button("🔍 Predict Persona")


# ---------------------------------------------------------
# PREDICTION EXECUTION
# ---------------------------------------------------------
if submit:
    st.markdown("### ⏳ Generating Prediction...")

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
        "FD_Amount": FD_Amount
    }], columns=FEATURE_COLUMNS)

    cluster_id = int(model.predict(input_data)[0])
    persona = PERSONA_DETAILS.get(cluster_id, {})

    st.success(f"### 🎯 Persona Identified: **{persona['name']}**")
    st.write(f"**Description:** {persona['description']}")

    st.subheader("💡 Recommended Actions")
    for rec in persona.get("recommendations", []):
        st.markdown(f"- ✅ {rec}")
