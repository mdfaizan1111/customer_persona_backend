import streamlit as st
import joblib
import pandas as pd
from persona_config import PERSONA_DETAILS

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Customer Persona Predictor",
    layout="wide",
    page_icon="💼"
)

# -------------- CUSTOM BANK-GRADE CSS --------------
st.markdown("""
<style>

body {
    background-color: #f5f7fa;
}

/* Section Headers */
h2 {
    color: #1a237e;
    font-weight: 700;
}

/* Persona Cards */
.persona-card {
    background: linear-gradient(135deg, #e8eaf6, #ffffff);
    padding: 18px;
    border-radius: 12px;
    border-left: 6px solid #283593;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.07);
    margin-bottom: 18px;
}

/* Prediction Box */
.result-box {
    background: linear-gradient(135deg, #e3f2fd, #ffffff);
    padding: 22px;
    border-radius: 12px;
    border-left: 6px solid #1565c0;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)


# ---------------- Load Model ----------------
@st.cache_data
def load_model():
    return joblib.load("model.pkl")

model = load_model()


# ---------------- FEATURE ORDER ----------------
FEATURE_COLUMNS = [
    "Age", "Gender", "City_Tier", "Occupation", "Annual_Income", "AMB",
    "Debit_Txn_Count", "Credit_Txn_Count", "UPI_Usage_Ratio",
    "ATM_Withdrawal_Count", "Failed_Txn_Count", "Mobile_App_Login",
    "Netbanking_Login", "Dormancy_Days", "Products_Held",
    "Credit_Card_Utilization", "EMI_Presence", "Insurance_Premium",
    "SIP_Amount", "FD_Amount"
]


# ---------------- HEADER ----------------
st.markdown("<h1 style='color:#1a237e;'>💼 Customer Persona Prediction System</h1>", unsafe_allow_html=True)
st.markdown("### Identify customer segments & drive precision marketing using bank-grade clustering intelligence.")
st.markdown("---")


# ---------------- PERSONA OVERVIEW ----------------
st.markdown("## 🌈 Customer Persona Overview")

columns = st.columns(2)
columns2 = st.columns(2)
persona_list = list(PERSONA_DETAILS.items())

def persona_card(col, pid, p):
    col.markdown(
        f"""
        <div class="persona-card">
            <h4>🔹 Persona {pid}: {p['name']}</h4>
            <p style="font-size:15px;">{p['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

persona_card(columns[0], *persona_list[0])
persona_card(columns[1], *persona_list[1])
persona_card(columns2[0], *persona_list[2])
persona_card(columns2[1], *persona_list[3])

st.markdown("---")


# ---------------- TOOLTIP HELP ----------------
FEATURE_META = {
    "Age": {"desc": "Customer age.", "reason": "Life stage indicator."},
    "Gender": {"desc": "Gender identity.", "reason": "Behavior segmentation only."},
    "City_Tier": {"desc": "City tier (1–3).", "reason": "Affluence signal."},
    "Occupation": {"desc": "Primary occupation.", "reason": "Income pattern."},
    "Annual_Income": {"desc": "Annual income (₹).", "reason": "Financial profile strength."},
    "AMB": {"desc": "Average monthly balance.", "reason": "Deposit relationship depth."},
    "Debit_Txn_Count": {"desc": "Outgoing transaction count.", "reason": "Activity measure."},
    "Credit_Txn_Count": {"desc": "Incoming credits.", "reason": "Salary/inflow dependency."},
    "UPI_Usage_Ratio": {"desc": "UPI adoption level.", "reason": "Digital maturity."},
    "ATM_Withdrawal_Count": {"desc": "ATM dependency.", "reason": "Cash behavior."},
    "Failed_Txn_Count": {"desc": "Failed transactions.", "reason": "Friction experience."},
    "Mobile_App_Login": {"desc": "App logins.", "reason": "Engagement."},
    "Netbanking_Login": {"desc": "Web logins.", "reason": "Digital usage depth."},
    "Dormancy_Days": {"desc": "Inactive days.", "reason": "Churn risk."},
    "Products_Held": {"desc": "Product count.", "reason": "Relationship breadth."},
    "Credit_Card_Utilization": {"desc": "Card utilization.", "reason": "Credit appetite."},
    "EMI_Presence": {"desc": "Active EMIs.", "reason": "Leverage level."},
    "Insurance_Premium": {"desc": "Insurance spend.", "reason": "Protection maturity."},
    "SIP_Amount": {"desc": "Monthly SIP.", "reason": "Investment maturity."},
    "FD_Amount": {"desc": "FD total value.", "reason": "Risk profile."},
}

def help_text(feature):
    meta = FEATURE_META.get(feature, {})
    return f"{meta.get('desc','')}\n\n**Reason:** {meta.get('reason','')}"


# ---------------- INPUT FORM ----------------
st.markdown("## 📋 Enter Customer Details")

with st.form("customer_form"):
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
        Failed_Txn_Count = st.number_input("Failed Txn Count", 0, 50, 1, help=help_text("Failed_Txn_Count"))
        Mobile_App_Login = st.number_input("App Logins", 0, 300, 20, help=help_text("Mobile_App_Login"))

    c4, c5, c6 = st.columns(3)

    with c4:
        Netbanking_Login = st.number_input("Netbanking Logins", 0, 300, 10, help=help_text("Netbanking_Login"))
        Dormancy_Days = st.number_input("Dormancy Days", 0, 365, 30, help=help_text("Dormancy_Days"))

    with c5:
        Products_Held = st.number_input("Products Held", 0, 10, 2, help=help_text("Products_Held"))
        Credit_Card_Utilization = st.number_input("Credit Card Utilization (%)", 0, 100, 40, help=help_text("Credit_Card_Utilization"))

    with c6:
        EMI_Presence = st.selectbox("EMI Presence", [0, 1], help=help_text("EMI_Presence"))
        Insurance_Premium = st.number_input("Insurance Premium", 0, 500000, 3000, help=help_text("Insurance_Premium"))
        SIP_Amount = st.number_input("SIP Amount", 0, 500000, 2000, help=help_text("SIP_Amount"))
        FD_Amount = st.number_input("FD Amount", 0, 10000000, 50000, help=help_text("FD_Amount"))

    submit = st.form_submit_button("🔍 Predict Persona")


# ---------------- PREDICTION ----------------
if submit:
    st.markdown("### 📊 Prediction Result")

    input_df = pd.DataFrame([{
        "Age": Age, "Gender": Gender, "City_Tier": City_Tier, "Occupation": Occupation,
        "Annual_Income": Annual_Income, "AMB": AMB,
        "Debit_Txn_Count": Debit_Txn_Count, "Credit_Txn_Count": Credit_Txn_Count,
        "UPI_Usage_Ratio": UPI_Usage_Ratio, "ATM_Withdrawal_Count": ATM_Withdrawal_Count,
        "Failed_Txn_Count": Failed_Txn_Count, "Mobile_App_Login": Mobile_App_Login,
        "Netbanking_Login": Netbanking_Login, "Dormancy_Days": Dormancy_Days,
        "Products_Held": Products_Held, "Credit_Card_Utilization": Credit_Card_Utilization,
        "EMI_Presence": EMI_Presence, "Insurance_Premium": Insurance_Premium,
        "SIP_Amount": SIP_Amount, "FD_Amount": FD_Amount
    }], columns=FEATURE_COLUMNS)

    cluster_id = int(model.predict(input_df)[0])
    persona = PERSONA_DETAILS.get(cluster_id, {})

    st.markdown(
        f"""
        <div class="result-box">
            <h3>🎯 Persona Identified: <b>{persona.get('name')}</b></h3>
            <p>{persona.get('description')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 💡 Recommended Marketing Strategies")
    for rec in persona.get("recommendations", []):
        st.markdown(f"- ✔️ {rec}")
