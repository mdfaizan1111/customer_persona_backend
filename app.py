import streamlit as st
import joblib
import pandas as pd
from persona_config import PERSONA_DETAILS  # persona names, descriptions, recommendations

st.set_page_config(page_title="Customer Persona Predictor", layout="wide")

# ------------------------------------------------------------------------------
# Load Model Once
# ------------------------------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

FEATURE_COLUMNS = [
    "Age", "Gender", "City_Tier", "Occupation", "Annual_Income", "AMB",
    "Debit_Txn_Count", "Credit_Txn_Count", "UPI_Usage_Ratio",
    "ATM_Withdrawal_Count", "Failed_Txn_Count", "Mobile_App_Login",
    "Netbanking_Login", "Dormancy_Days", "Products_Held",
    "Credit_Card_Utilization", "EMI_Presence", "Insurance_Premium",
    "SIP_Amount", "FD_Amount"
]

# ------------------------------------------------------------------------------
# Feature Meta Information
# ------------------------------------------------------------------------------
FEATURE_META = {
    "Age": {"desc": "Customer age in years.", "reason": "Age indicates life stage & financial needs."},
    "Gender": {"desc": "Self-identified gender.", "reason": "Used only for behaviour segmentation."},
    "City_Tier": {"desc": "Tier of city (1=metro, 3=rural).", "reason": "Captures economic environment."},
    "Occupation": {"desc": "Primary occupation.", "reason": "Impacts income stability & financial behaviour."},
    "Annual_Income": {"desc": "Annual income in ₹.", "reason": "Predicts product appetite."},
    "AMB": {"desc": "Average Monthly Balance.", "reason": "Indicates depth of engagement."},
    "Debit_Txn_Count": {"desc": "Monthly debit transactions.", "reason": "Reflects activity levels."},
    "Credit_Txn_Count": {"desc": "Monthly credit transactions.", "reason": "Salary & inflow indicator."},
    "UPI_Usage_Ratio": {"desc": "UPI transaction share.", "reason": "Digital adoption metric."},
    "ATM_Withdrawal_Count": {"desc": "ATM cash withdrawals.", "reason": "Cash dependency indicator."},
    "Failed_Txn_Count": {"desc": "Failed transactions.", "reason": "Friction leading to churn risk."},
    "Mobile_App_Login": {"desc": "Mobile app logins.", "reason": "Digital engagement."},
    "Netbanking_Login": {"desc": "Netbanking logins.", "reason": "Web-based behaviour."},
    "Dormancy_Days": {"desc": "Days since last active usage.", "reason": "Early dormancy detection."},
    "Products_Held": {"desc": "Number of bank products used.", "reason": "Relationship depth."},
    "Credit_Card_Utilization": {"desc": "Credit card usage %.", "reason": "Credit appetite indicator."},
    "EMI_Presence": {"desc": "Active EMIs.", "reason": "Cash flow stress & credit penetration."},
    "Insurance_Premium": {"desc": "Insurance spending.", "reason": "Protection maturity."},
    "SIP_Amount": {"desc": "Monthly SIP amount.", "reason": "Investment maturity."},
    "FD_Amount": {"desc": "Total FD holdings.", "reason": "Conservative savings behaviour."},
}


def help_text(feature):
    meta = FEATURE_META.get(feature, {})
    return f"{meta.get('desc','')}\n\n**Reason:** {meta.get('reason','')}"

# ------------------------------------------------------------------------------
# Display Persona Cards (BEFORE form)
# ------------------------------------------------------------------------------
st.title("🧠 Customer Persona Prediction App")
st.write("Predict which persona a customer belongs to and get targeted marketing strategies.")

st.markdown("## 👥 The Four Customer Personas We Identified")

persona_cols = st.columns(2)

for idx, (pid, pdata) in enumerate(PERSONA_DETAILS.items()):
    col = persona_cols[idx % 2]
    with col:
        st.markdown(
            f"""
            <div style="background:#f0f2f6;padding:15px;border-radius:10px;margin-bottom:20px;
            border-left:6px solid #4A90E2;">
                <h3 style="color:#333;">🔹 {pdata['name']}</h3>
                <p style="color:#555;font-size:15px;">{pdata['description']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# ------------------------------------------------------------------------------
# Prevent Auto-Rerun of Predictions
# ------------------------------------------------------------------------------
if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False


# ------------------------------------------------------------------------------
# INPUT FORM
# ------------------------------------------------------------------------------
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
        ATM_Withdrawal_Count = st.number_input("ATM Withdrawal Count", 0, 50, 2, help=help_text("ATM_Withdrawal_Count"))
        Failed_Txn_Count = st.number_input("Failed Txn Count", 0, 50, 1, help=help_text("Failed_Txn_Count"))
        Mobile_App_Login = st.number_input("Mobile App Logins", 0, 300, 20, help=help_text("Mobile_App_Login"))

    st.markdown("### 🔐 Banking Behaviour & Relationship")
    col4, col5, col6 = st.columns(3)

    with col4:
        Netbanking_Login = st.number_input("Netbanking Logins", 0, 300, 10, help=help_text("Netbanking_Login"))
        Dormancy_Days = st.number_input("Dormancy Days", 0, 365, 30, help=help_text("Dormancy_Days"))

    with col5:
        Products_Held = st.number_input("Products Held", 0, 10, 2, help=help_text("Products_Held"))
        Credit_Card_Utilization = st.number_input("Credit Utilization (%)", 0, 100, 40, help=help_text("Credit_Card_Utilization"))

    with col6:
        EMI_Presence = st.selectbox("EMI Presence (0/1)", [0, 1], help=help_text("EMI_Presence"))
        Insurance_Premium = st.number_input("Insurance Premium", 0, 500000, 3000, help=help_text("Insurance_Premium"))
        SIP_Amount = st.number_input("SIP Amount", 0, 500000, 2000, help=help_text("SIP_Amount"))
        FD_Amount = st.number_input("FD Amount", 0, 10000000, 50000, help=help_text("FD_Amount"))

    submit = st.form_submit_button("🔍 Predict Persona")

# ------------------------------------------------------------------------------
# Prediction Logic with Auto-Rerun FIX
# ------------------------------------------------------------------------------
if submit:
    st.session_state.prediction_done = True

if st.session_state.prediction_done:

    input_data = pd.DataFrame([{
        "Age": Age, "Gender": Gender, "City_Tier": City_Tier, "Occupation": Occupation,
        "Annual_Income": Annual_Income, "AMB": AMB, "Debit_Txn_Count": Debit_Txn_Count,
        "Credit_Txn_Count": Credit_Txn_Count, "UPI_Usage_Ratio": UPI_Usage_Ratio,
        "ATM_Withdrawal_Count": ATM_Withdrawal_Count, "Failed_Txn_Count": Failed_Txn_Count,
        "Mobile_App_Login": Mobile_App_Login, "Netbanking_Login": Netbanking_Login,
        "Dormancy_Days": Dormancy_Days, "Products_Held": Products_Held,
        "Credit_Card_Utilization": Credit_Card_Utilization, "EMI_Presence": EMI_Presence,
        "Insurance_Premium": Insurance_Premium, "SIP_Amount": SIP_Amount, "FD_Amount": FD_Amount,
    }], columns=FEATURE_COLUMNS)

    cluster_id = int(model.predict(input_data)[0])
    persona = PERSONA_DETAILS.get(cluster_id, {})

    # Results
    st.success(f"### 🎯 Predicted Persona: **{persona.get('name','Unknown Persona')}**")
    st.write(f"**{persona.get('description','')}**")

    st.markdown("---")
    st.subheader("💡 Recommended Marketing Strategies")

    for r in persona.get("recommendations", []):
        st.markdown(f"- ✅ {r}")

# Reset Button
if st.button("Reset Form"):
    st.session_state.prediction_done = False
