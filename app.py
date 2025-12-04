import streamlit as st
import joblib
import pandas as pd
from persona_config import PERSONA_DETAILS  # your persona dict

# --------------------------------------------------------------------
# BASIC PAGE CONFIG
# --------------------------------------------------------------------
st.set_page_config(
    page_title="Customer Persona Predictor",
    layout="wide",
)

# --------------------------------------------------------------------
# LOAD MODEL ONCE (CACHED)
# --------------------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# Column order expected by the pipeline
FEATURE_COLUMNS = [
    "Age", "Gender", "City_Tier", "Occupation", "Annual_Income", "AMB",
    "Debit_Txn_Count", "Credit_Txn_Count", "UPI_Usage_Ratio",
    "ATM_Withdrawal_Count", "Failed_Txn_Count", "Mobile_App_Login",
    "Netbanking_Login", "Dormancy_Days", "Products_Held",
    "Credit_Card_Utilization", "EMI_Presence", "Insurance_Premium",
    "SIP_Amount", "FD_Amount"
]

# --------------------------------------------------------------------
# FEATURE META (HELP TEXT)
# --------------------------------------------------------------------
FEATURE_META = {
    "Age": {
        "desc": "Customer age in years.",
        "reason": "Age proxies life-stage and typical product needs."
    },
    "Gender": {
        "desc": "Self-identified gender.",
        "reason": "Used only for segmentation, not pricing or eligibility."
    },
    "City_Tier": {
        "desc": "Tier of customer’s city (1 = metro, 3 = semi-urban / rural).",
        "reason": "Captures economic context and channel behaviour."
    },
    "Occupation": {
        "desc": "Primary occupation type.",
        "reason": "Drives income stability and spending pattern."
    },
    "Annual_Income": {
        "desc": "Approximate annual income (₹).",
        "reason": "Key driver of financial capacity and product appetite."
    },
    "AMB": {
        "desc": "Average Monthly Balance maintained in the account.",
        "reason": "Indicates depth of relationship and deposit potential."
    },
    "Debit_Txn_Count": {
        "desc": "Monthly count of outgoing debit transactions.",
        "reason": "Proxy for account activity and spend usage."
    },
    "Credit_Txn_Count": {
        "desc": "Monthly count of incoming credit transactions.",
        "reason": "Captures salary credits, inflows and business receipts."
    },
    "UPI_Usage_Ratio": {
        "desc": "Share of transactions done via UPI (0–1).",
        "reason": "Direct measure of digital adoption."
    },
    "ATM_Withdrawal_Count": {
        "desc": "Monthly ATM cash withdrawals.",
        "reason": "Indicates cash dependency vs digital spending."
    },
    "Failed_Txn_Count": {
        "desc": "Monthly failed transactions.",
        "reason": "High failures can mean friction and dissatisfaction."
    },
    "Mobile_App_Login": {
        "desc": "Monthly mobile banking logins.",
        "reason": "Core digital engagement metric."
    },
    "Netbanking_Login": {
        "desc": "Monthly netbanking logins.",
        "reason": "Captures web-based digital activity."
    },
    "Dormancy_Days": {
        "desc": "Days since last successful transaction.",
        "reason": "Early signal for dormancy or churn risk."
    },
    "Products_Held": {
        "desc": "Number of products held (loan, card, FD, etc.).",
        "reason": "Relationship depth and cross-sell base."
    },
    "Credit_Card_Utilization": {
        "desc": "Credit card utilization percentage.",
        "reason": "Shows credit appetite and repayment behaviour."
    },
    "EMI_Presence": {
        "desc": "Whether customer has active EMIs (0 = No, 1 = Yes).",
        "reason": "Indicates leverage level and credit penetration."
    },
    "Insurance_Premium": {
        "desc": "Total insurance premium outflow.",
        "reason": "Shows protection product penetration and upsell scope."
    },
    "SIP_Amount": {
        "desc": "Monthly SIP amount in mutual funds.",
        "reason": "Proxy for investment maturity and risk appetite."
    },
    "FD_Amount": {
        "desc": "Total fixed deposit holdings.",
        "reason": "Captures conservative savings and liquidity buffer."
    },
}


def help_text(name: str) -> str:
    meta = FEATURE_META.get(name, {})
    return f"{meta.get('desc', '')}\n\n**Why used:** {meta.get('reason', '')}"


# --------------------------------------------------------------------
# HEADER + PERSONA OVERVIEW CARDS
# --------------------------------------------------------------------
st.title("🧠 Customer Persona Prediction App")

st.write(
    "Use this tool to classify a retail banking customer into one of the pre-defined "
    "personas and view suggested marketing & cross-sell actions."
)

st.markdown("### 📌 Persona Archetypes")

cols = st.columns(len(PERSONA_DETAILS))
for idx, (cluster_id, persona) in enumerate(PERSONA_DETAILS.items()):
    with cols[idx]:
        st.markdown(
            f"""
            <div style="
                border-radius: 12px;
                padding: 12px;
                border: 1px solid #e0e0e0;
                background: linear-gradient(135deg, #f8fafc, #eef2ff);
                height: 100%;
            ">
                <h4 style="margin-bottom:4px;">{persona.get('name','Persona')}</h4>
                <p style="font-size:0.85rem; margin-bottom:4px;">
                    {persona.get('description','')}
                </p>
                <p style="font-size:0.78rem; color:#555;">
                    Example plays:
                    <ul style="margin-left:-18px; font-size:0.78rem;">
                        {''.join([f"<li>{r}</li>" for r in persona.get('recommendations', [])[:2]])}
                    </ul>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# --------------------------------------------------------------------
# INPUT FORM (GROUPED SECTIONS)
# --------------------------------------------------------------------
with st.form("customer_form"):
    st.subheader("📋 Capture Customer Snapshot")

    # --- Demographics & Profile ---
    st.markdown("#### 👤 Demographics & Profile")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        Age = st.number_input("Age", 18, 100, 30, help=help_text("Age"))
    with c2:
        Gender = st.selectbox("Gender", ["Male", "Female", "Other"], help=help_text("Gender"))
    with c3:
        City_Tier = st.selectbox("City Tier", [1.0, 2.0, 3.0], index=0, help=help_text("City_Tier"))
    with c4:
        Occupation = st.selectbox(
            "Occupation",
            ["Salaried", "Self-Employed", "Business Owner"],
            help=help_text("Occupation")
        )

    # --- Income & Account Activity ---
    st.markdown("#### 💰 Income & Account Activity")
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        Annual_Income = st.number_input(
            "Annual Income (₹)", 100000, 10000000, 800000, step=50000,
            help=help_text("Annual_Income")
        )
    with c6:
        AMB = st.number_input(
            "Average Monthly Balance (₹)", 0, 1000000, 50000, step=5000,
            help=help_text("AMB")
        )
    with c7:
        Debit_Txn_Count = st.number_input(
            "Monthly Debit Txn Count", 0, 300, 10,
            help=help_text("Debit_Txn_Count")
        )
    with c8:
        Credit_Txn_Count = st.number_input(
            "Monthly Credit Txn Count", 0, 300, 5,
            help=help_text("Credit_Txn_Count")
        )

    # --- Digital & Channel Behaviour ---
    st.markdown("#### 📱 Digital & Channel Behaviour")
    c9, c10, c11, c12 = st.columns(4)
    with c9:
        UPI_Usage_Ratio = st.slider(
            "UPI Usage Ratio", 0.0, 1.0, 0.5,
            help=help_text("UPI_Usage_Ratio")
        )
    with c10:
        Mobile_App_Login = st.number_input(
            "Mobile App Logins (per month)", 0, 300, 20,
            help=help_text("Mobile_App_Login")
        )
    with c11:
        Netbanking_Login = st.number_input(
            "Netbanking Logins (per month)", 0, 300, 10,
            help=help_text("Netbanking_Login")
        )
    with c12:
        ATM_Withdrawal_Count = st.number_input(
            "ATM Withdrawals (per month)", 0, 50, 2,
            help=help_text("ATM_Withdrawal_Count")
        )

    # --- Relationship Depth & Risk ---
    st.markdown("#### 🧩 Relationship Depth & Risk")
    c13, c14, c15, c16 = st.columns(4)
    with c13:
        Products_Held = st.number_input(
            "Products Held (count)", 0, 10, 2,
            help=help_text("Products_Held")
        )
        Dormancy_Days = st.number_input(
            "Dormancy Days", 0, 365, 30,
            help=help_text("Dormancy_Days")
        )
    with c14:
        Credit_Card_Utilization = st.number_input(
            "Credit Card Utilization (%)", 0, 100, 40,
            help=help_text("Credit_Card_Utilization")
        )
        Failed_Txn_Count = st.number_input(
            "Failed Txn Count (per month)", 0, 50, 1,
            help=help_text("Failed_Txn_Count")
        )
    with c15:
        EMI_Presence = st.selectbox(
            "EMI Presence (0 = No, 1 = Yes)",
            [0, 1],
            help=help_text("EMI_Presence")
        )
        Insurance_Premium = st.number_input(
            "Insurance Premium (₹)", 0, 500000, 3000, step=500,
            help=help_text("Insurance_Premium")
        )
    with c16:
        SIP_Amount = st.number_input(
            "SIP Amount (₹)", 0, 500000, 2000, step=500,
            help=help_text("SIP_Amount")
        )
        FD_Amount = st.number_input(
            "FD Amount (₹)", 0, 10000000, 50000, step=10000,
            help=help_text("FD_Amount")
        )

    submit = st.form_submit_button("🔍 Predict Persona")

# --------------------------------------------------------------------
# PREDICTION (ONLY ON BUTTON CLICK) + SESSION STATE STORAGE
# --------------------------------------------------------------------
if submit:
    # Prepare input in a DataFrame with correct column order
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
    persona = PERSONA_DETAILS.get(cluster_id, {})

    # Save to session_state so result persists across reruns
    st.session_state["last_cluster_id"] = cluster_id
    st.session_state["last_persona"] = persona

# --------------------------------------------------------------------
# RESULT DISPLAY (PERSISTS EVEN IF APP RERUNS)
# --------------------------------------------------------------------
if "last_persona" in st.session_state:
    persona = st.session_state["last_persona"]
    cluster_id = st.session_state["last_cluster_id"]

    st.markdown("---")
    st.markdown("### 📊 Latest Prediction Result")

    st.markdown(
        f"""
        <div style="
            border-radius: 14px;
            padding: 16px 18px;
            border: 1px solid #d4d4d8;
            background: linear-gradient(135deg, #f9fafb, #eef2ff);
        ">
            <h3 style="margin-bottom:6px;">🎯 Persona: {persona.get('name', 'Unknown Persona')}</h3>
            <p style="margin-bottom:6px;"><b>Cluster ID:</b> {cluster_id}</p>
            <p style="font-size:0.95rem; margin-bottom:8px;">
                {persona.get('description', '')}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 💡 Recommended Marketing / Cross-sell Plays")
    for rec in persona.get("recommendations", []):
        st.markdown(f"- ✅ {rec}")
else:
    st.info("Fill the form above and click **Predict Persona** to see the result here.")
