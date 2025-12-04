import streamlit as st
import joblib
import pandas as pd
from persona_config import PERSONA_DETAILS

st.set_page_config(page_title="Customer Persona Predictor", layout="wide")

# ---------------- Load Trained Model ----------------
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# Feature order exactly as the model expects
FEATURE_COLUMNS = [
    "Age", "Gender", "City_Tier", "Occupation", "Annual_Income", "AMB",
    "Debit_Txn_Count", "Credit_Txn_Count", "UPI_Usage_Ratio",
    "ATM_Withdrawal_Count", "Failed_Txn_Count", "Mobile_App_Login",
    "Netbanking_Login", "Dormancy_Days", "Products_Held",
    "Credit_Card_Utilization", "EMI_Presence", "Insurance_Premium",
    "SIP_Amount", "FD_Amount"
]

# ---------------- Feature meta ----------------
FEATURE_META = {
    "Age": {"desc": "Customer age in years.", "reason": "Life stage & product needs."},
    "Gender": {"desc": "Self-identified gender.", "reason": "Used only for segmentation."},
    "City_Tier": {"desc": "City affluence level.", "reason": "Economic environment indicator."},
    "Occupation": {"desc": "Primary occupation.", "reason": "Income stability & spending."},
    "Annual_Income": {"desc": "Annual income (₹).", "reason": "Financial capacity indicator."},
    "AMB": {"desc": "Average monthly balance.", "reason": "Banking relationship depth."},
    "Debit_Txn_Count": {"desc": "Monthly debit transactions.", "reason": "Spending behaviour."},
    "Credit_Txn_Count": {"desc": "Monthly credit transactions.", "reason": "Inflow pattern."},
    "UPI_Usage_Ratio": {"desc": "Share of UPI transactions.", "reason": "Digital adoption."},
    "ATM_Withdrawal_Count": {"desc": "ATM cash withdrawals.", "reason": "Cash dependency."},
    "Failed_Txn_Count": {"desc": "Failed monthly transactions.", "reason": "Friction indicator."},
    "Mobile_App_Login": {"desc": "Mobile app logins.", "reason": "Digital engagement."},
    "Netbanking_Login": {"desc": "Netbanking logins.", "reason": "Web engagement."},
    "Dormancy_Days": {"desc": "Days since last activity.", "reason": "Dormancy risk."},
    "Products_Held": {"desc": "Number of products held.", "reason": "Relationship depth."},
    "Credit_Card_Utilization": {"desc": "Card utilization %.", "reason": "Credit appetite."},
    "EMI_Presence": {"desc": "Active EMI indicator.", "reason": "Borrowing status."},
    "Insurance_Premium": {"desc": "Insurance spending.", "reason": "Protection coverage."},
    "SIP_Amount": {"desc": "Monthly SIP amount.", "reason": "Investment maturity."},
    "FD_Amount": {"desc": "Total FD amount.", "reason": "Savings stability."},
}


def help_text(feature_name):
    meta = FEATURE_META.get(feature_name, {})
    return f"{meta.get('desc', '')}\n\n**Reason:** {meta.get('reason', '')}"


# ------------------------ HEADER ------------------------
st.title("🧠 Customer Persona Prediction App")
st.write("Predict customer persona + get actionable marketing recommendations.")

st.markdown("---")

# -------------------------------------------------------------------
# ⭐ BEAUTIFUL PERSONA CARDS — SHOWN BEFORE USER INPUT
# -------------------------------------------------------------------

st.subheader("🌈 Four Customer Personas Used in This Model")

persona_colors = ["#FDEBD0", "#D6EAF8", "#E8DAEF", "#D5F5E3"]

cols = st.columns(4)

for idx, (cluster_id, details) in enumerate(PERSONA_DETAILS.items()):
    color = persona_colors[idx % len(persona_colors)]
    with cols[idx]:
        st.markdown(
            f"""
            <div style='padding:15px; border-radius:10px; background-color:{color};'>
                <h4 style='margin-bottom:5px;'>{details.get("name", "Persona")}</h4>
                <p style='font-size:14px;'>{details.get("description", "")[:120]}...</p>
            </div>
            """,
            unsafe_allow_html=True
        )

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
        Annual_Income = st.number_input("Annual Income (₹)", 100000, 10000000, 800000)
        AMB = st.number_input("Average Monthly Balance (₹)", 0, 1000000, 50000)
        Debit_Txn_Count = st.number_input("Debit Txn Count", 0, 300, 10)
        Credit_Txn_Count = st.number_input("Credit Txn Count", 0, 300, 5)

    with col3:
        UPI_Usage_Ratio = st.slider("UPI Usage Ratio", 0.0, 1.0, 0.5)
        ATM_Withdrawal_Count = st.number_input("ATM Withdrawals", 0, 50, 2)
        Failed_Txn_Count = st.number_input("Failed Transactions", 0, 50, 1)
        Mobile_App_Login = st.number_input("Mobile App Logins", 0, 300, 20)

    st.markdown("### 🔐 Banking Behaviour & Relationship")

    col4, col5, col6 = st.columns(3)

    with col4:
        Netbanking_Login = st.number_input("Netbanking Logins", 0, 300, 10)
        Dormancy_Days = st.number_input("Dormancy Days", 0, 365, 30)

    with col5:
        Products_Held = st.number_input("Products Held", 0, 10, 2)
        Credit_Card_Utilization = st.number_input("Credit Card Utilization (%)", 0, 100, 40)

    with col6:
        EMI_Presence = st.selectbox("EMI Presence", [0, 1])
        Insurance_Premium = st.number_input("Insurance Premium", 0, 500000, 3000)
        SIP_Amount = st.number_input("SIP Amount", 0, 500000, 2000)
        FD_Amount = st.number_input("FD Amount", 0, 10000000, 50000)

    submit = st.form_submit_button("🔍 Predict Persona")

# ------------------------ PREDICTION LOGIC ------------------------
if submit:
    st.markdown("### ⏳ Generating Prediction...")

    input_data = pd.DataFrame([{
        "Age": Age, "Gender": Gender, "City_Tier": City_Tier,
        "Occupation": Occupation, "Annual_Income": Annual_Income,
        "AMB": AMB, "Debit_Txn_Count": Debit_Txn_Count,
        "Credit_Txn_Count": Credit_Txn_Count, "UPI_Usage_Ratio": UPI_Usage_Ratio,
        "ATM_Withdrawal_Count": ATM_Withdrawal_Count, "Failed_Txn_Count": Failed_Txn_Count,
        "Mobile_App_Login": Mobile_App_Login, "Netbanking_Login": Netbanking_Login,
        "Dormancy_Days": Dormancy_Days, "Products_Held": Products_Held,
        "Credit_Card_Utilization": Credit_Card_Utilization, "EMI_Presence": EMI_Presence,
        "Insurance_Premium": Insurance_Premium, "SIP_Amount": SIP_Amount, "FD_Amount": FD_Amount
    }], columns=FEATURE_COLUMNS)

    cluster_id = int(model.predict(input_data)[0])
    persona = PERSONA_DETAILS.get(cluster_id, {})

    st.success(f"### 🎯 Predicted Persona: **{persona.get('name', 'Unknown')}**")
    st.write(f"**Description:** {persona.get('description', '')}")

    st.markdown("---")
    st.subheader("💡 Recommended Marketing Strategies")

    for rec in persona.get("recommendations", []):
        st.markdown(f"- ✅ {rec}")
