import streamlit as st
import joblib
import pandas as pd
from persona_config import PERSONA_DETAILS

# ---------------------------------------------------------
# PAGE CONFIG (Fixes LinkedIn rich preview + metadata)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Customer Persona Predictor",
    page_icon="🧠",
    layout="wide",
)

st.markdown("""
<meta name="title" content="Customer Persona Predictor | ML Segmentation Demo">
<meta name="description" content="Interactive app to classify customers into data-driven personas using ML clustering. Built with Streamlit + Python.">
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD MODEL SAFELY (cached)
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# ---------------------------------------------------------
# FEATURE ORDER (must match model training)
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
# CLUSTER MEDIAN FACTS (from your screenshots)
# ---------------------------------------------------------
PERSONA_FACTS = {
    0: {
        "Age": 28,
        "Occupation": "Salaried (65%)",
        "UPI Usage": "0.76",
        "Mobile App Logins": 35,
        "AMB": "₹32,000",
        "SIP Amount": "₹1,200",
        "FD Amount": "₹10,000",
        "ATM Withdrawals": 1,
    },
    1: {
        "Age": 45,
        "Occupation": "Business Owner (58%)",
        "FD Amount": "₹8,50,000",
        "AMB": "₹1,20,000",
        "UPI Usage": "0.32",
        "ATM Withdrawals": 6,
        "SIP Amount": "₹2,500",
    },
    2: {
        "Age": 34,
        "Occupation": "Salaried (72%)",
        "Income": "₹18,00,000",
        "SIP Amount": "₹12,000",
        "Mobile App Logins": 68,
        "Credit Card Utilization": "48%",
        "FD Amount": "₹75,000",
        "UPI Usage": "0.84",
    },
    3: {
        "Age": 31,
        "Occupation": "Self-Employed (52%)",
        "ATM Withdrawals": 11,
        "UPI Usage": "0.41",
        "Mobile App Logins": 16,
        "AMB": "₹18,000",
        "FD Amount": "₹22,000",
    }
}

# ---------------------------------------------------------
# APP HEADER
# ---------------------------------------------------------
st.title("🧠 Customer Persona Prediction App")
st.write(
    "Classify customers into **data-driven personas** using ML segmentation. "
    "Enter customer attributes to generate a live persona prediction."
)

# ---------------------------------------------------------
# PERSONA OVERVIEW GRID
# ---------------------------------------------------------
st.markdown("## 📌 Persona Archetypes Overview")

cols = st.columns(4)
for idx, (cluster_id, persona) in enumerate(PERSONA_DETAILS.items()):

    facts = PERSONA_FACTS.get(cluster_id, {})
    median_html = (
        "<p style='margin:4px 0 2px; font-weight:600;'>Median Snapshot:</p>"
        "<ul style='margin-left:-10px; font-size:0.80rem;'>"
        + "".join([f"<li><b>{k}:</b> {v}</li>" for k, v in facts.items()])
        + "</ul>"
    )

    with cols[idx]:
        st.markdown(
            f"""
            <div style="
                border-radius: 14px;
                padding: 14px;
                border: 1px solid #ddd;
                background: #f7f9fc;
                min-height: 280px;
            ">
                <h3>{persona.get("icon","")} {persona.get("name","")}</h3>
                <p style="font-size:0.85rem;">{persona.get("description","")}</p>
                {median_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# ---------------------------------------------------------
# INPUT FORM
# ---------------------------------------------------------
st.subheader("📋 Enter Customer Details")

with st.form("customer_form", clear_on_submit=False):

    # DEMOGRAPHICS
    st.markdown("### 👤 Demographics & Profile")
    c1, c2, c3, c4 = st.columns(4)
    Age = c1.number_input("Age", 18, 100, 30)
    Gender = c2.selectbox("Gender", ["Male", "Female", "Other"])
    City_Tier = c3.selectbox("City Tier", [1.0, 2.0, 3.0])
    Occupation = c4.selectbox("Occupation", ["Salaried", "Self-Employed", "Business Owner"])

    # INCOME & ACCOUNT ACTIVITY
    st.markdown("### 💰 Income & Account Activity")
    c5, c6, c7, c8 = st.columns(4)
    Annual_Income = c5.number_input("Annual Income (₹)", 100000, 50000000, 800000, step=50000)
    AMB = c6.number_input("Average Monthly Balance (₹)", 0, 5000000, 50000, step=5000)
    Debit_Txn_Count = c7.number_input("Monthly Debit Txn Count", 0, 300, 10)
    Credit_Txn_Count = c8.number_input("Monthly Credit Txn Count", 0, 300, 5)

    # DIGITAL BEHAVIOUR
    st.markdown("### 📱 Digital & Channel Behaviour")
    c9, c10, c11, c12 = st.columns(4)
    UPI_Usage_Ratio = c9.slider("UPI Usage Ratio", 0.0, 1.0, 0.5)
    Mobile_App_Login = c10.number_input("Mobile App Logins (per month)", 0, 300, 20)
    Netbanking_Login = c11.number_input("Netbanking Logins (per month)", 0, 300, 10)
    ATM_Withdrawal_Count = c12.number_input("ATM Withdrawals (per month)", 0, 50, 2)

    # RELATIONSHIP DEPTH
    st.markdown("### 🧩 Relationship Depth & Risk")
    c13, c14, c15, c16 = st.columns(4)
    Products_Held = c13.number_input("Products Held", 0, 10, 2)
    Dormancy_Days = c13.number_input("Dormancy Days", 0, 365, 30)
    Credit_Card_Utilization = c14.number_input("Credit Card Utilization (%)", 0, 100, 40)
    Failed_Txn_Count = c14.number_input("Failed Txn Count", 0, 50, 1)
    EMI_Presence = c15.selectbox("EMI Presence", [0, 1])
    Insurance_Premium = c15.number_input("Insurance Premium (₹)", 0, 500000, 3000)
    SIP_Amount = c16.number_input("SIP Amount (₹)", 0, 300000, 2000)
    FD_Amount = c16.number_input("FD Amount (₹)", 0, 20000000, 50000)

    submit = st.form_submit_button("🔍 Predict Persona")

# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------
if submit:
    input_df = pd.DataFrame([{
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

    cluster_id = int(model.predict(input_df)[0])
    st.session_state["cluster_id"] = cluster_id

# ---------------------------------------------------------
# RESULT DISPLAY (NO MEDIAN FACTS HERE)
# ---------------------------------------------------------
if "cluster_id" in st.session_state:
    cid = st.session_state["cluster_id"]
    persona = PERSONA_DETAILS.get(cid, {})

    st.markdown("---")
    st.markdown("## 🎯 Latest Prediction Result")

    st.markdown(
        f"""
        <div style="
            border-radius: 14px;
            padding: 18px;
            border: 1px solid #ccc;
            background: #f9fafb;
        ">
            <h2>{persona.get("icon","")} Persona: {persona.get("name","")}</h2>
            <p><b>Cluster ID:</b> {cid}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 💡 Recommended Actions")
    for rec in persona.get("recommendations", []):
        st.markdown(f"- {rec}")

else:
    st.info("Fill the form and click **Predict Persona** to see results.")
