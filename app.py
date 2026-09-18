import streamlit as st

from src.agent import LumaAssistAgent


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="LumaAssist | LumaCart",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #0f172a;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #293548;
}

[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

.main-title {
    color: #f8fafc;
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.main-subtitle {
    color: #94a3b8;
    font-size: 16px;
    margin-bottom: 25px;
}

.brand-highlight {
    color: #c4b5fd;
}

.welcome-card {
    background: linear-gradient(135deg, #1e293b, #172033);
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 25px;
}

.welcome-title {
    color: #f8fafc;
    font-size: 25px;
    font-weight: 650;
    margin-bottom: 10px;
}

.welcome-text {
    color: #cbd5e1;
    font-size: 15px;
    line-height: 1.7;
}

.capability-card {
    background-color: #172033;
    border: 1px solid #2d3a4f;
    border-radius: 14px;
    padding: 18px;
    min-height: 125px;
}

.capability-title {
    color: #f1f5f9;
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 8px;
}

.capability-text {
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.5;
}

.sidebar-brand {
    color: #f8fafc;
    font-size: 25px;
    font-weight: 700;
}

.sidebar-subtitle {
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 22px;
}

.sidebar-section {
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 22px;
    margin-bottom: 10px;
}

.sidebar-info {
    color: #cbd5e1;
    font-size: 13px;
    line-height: 1.8;
}

[data-testid="stChatMessage"] {
    border: 1px solid #293548;
    border-radius: 16px;
    margin-bottom: 12px;
}

[data-testid="stChatMessageContent"] {
    color: #e5e7eb;
}

.stButton > button {
    border-radius: 10px;
    border: 1px solid #3b4960;
    background-color: #1e293b;
    color: #e2e8f0;
}

.stButton > button:hover {
    border-color: #a78bfa;
    color: white;
}

.tool-status {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 8px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# Session State
# ============================================================

if "agent" not in st.session_state:
    st.session_state.agent = LumaAssistAgent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# Helper Functions
# ============================================================

def clear_conversation():

    st.session_state.agent = LumaAssistAgent()
    st.session_state.chat_history = []


def display_message(role, content):

    with st.chat_message(role):
        st.markdown(content)


def process_user_message(user_input):

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    display_message(
        role="user",
        content=user_input,
    )

    with st.chat_message("assistant"):

        with st.spinner("LumaAssist is thinking..."):

            try:

                response = st.session_state.agent.chat(
                    user_input
                )

            except Exception as error:

                response = (
                    "Sorry, something went wrong while "
                    "processing your request."
                )

                st.error(str(error))

        st.markdown(response)

        # Discreet tool activity
        tool_activity = getattr(
            st.session_state.agent,
            "last_tool_activity",
            [],
        )

        if tool_activity:

            unique_tools = list(
                dict.fromkeys(tool_activity)
            )

            st.markdown(
                (
                    '<div class="tool-status">'
                    "✓ Assistance tools used: "
                    + ", ".join(unique_tools)
                    + "</div>"
                ),
                unsafe_allow_html=True,
            )

        # Sources
        sources = getattr(
            st.session_state.agent,
            "last_sources",
            [],
        )

        if sources:

            with st.expander("View supporting information"):

                for source in sources:

                    st.markdown(
                        f"- {source}"
                    )

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.markdown(
        """
<div class="sidebar-brand">✦ LumaAssist</div>
<div class="sidebar-subtitle">LumaCart Customer Support</div>
""",
        unsafe_allow_html=True,
    )

    if st.button(
        "＋ New Conversation",
        use_container_width=True,
    ):

        clear_conversation()
        st.rerun()

    st.markdown(
        '<div class="sidebar-section">Quick Questions</div>',
        unsafe_allow_html=True,
    )

    suggested_questions = [
        "What payment methods are available?",
        "How long does shipping take to Cairo?",
        "What is your return policy?",
        "Show me the available products.",
        "Calculate an order with 800 EGP and 10% discount.",
        "Convert 100 USD to EUR.",
    ]

    for index, question in enumerate(
        suggested_questions
    ):

        if st.button(
            question,
            key=f"sidebar_question_{index}",
            use_container_width=True,
        ):

            st.session_state.pending_question = question
            st.rerun()

    st.markdown(
        '<div class="sidebar-section">Capabilities</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="sidebar-info">
✓ Product and policy questions<br>
✓ Shipping and returns<br>
✓ Order calculations<br>
✓ Live currency conversion<br>
✓ Conversation memory<br>
✓ Knowledge-base grounding
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">Company Information</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="sidebar-info">
<b>Company:</b> LumaCart<br>
<b>Location:</b> Cairo, Egypt<br>
<b>Support:</b> support@lumacart.example<br>
<b>Hours:</b> Sunday–Thursday<br>
<b>Time:</b> 9 AM–6 PM Egypt time
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">Privacy Note</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="sidebar-info">
Please do not share sensitive personal,
payment, or account information.
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# Main Header
# ============================================================

st.markdown(
    """
<div class="main-title">
Welcome to <span class="brand-highlight">LumaAssist</span>
</div>

<div class="main-subtitle">
Your intelligent customer-support assistant for LumaCart.
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# Welcome Screen
# ============================================================

if not st.session_state.chat_history:

    st.markdown(
        """
<div class="welcome-card">
<div class="welcome-title">How can we help you today?</div>

<div class="welcome-text">
Ask about LumaCart products, shipping, returns,
payment methods, order calculations, or currency conversion.
LumaAssist uses company knowledge and specialized tools
to provide helpful answers.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
<div class="capability-card">
<div class="capability-title">Product & Policies</div>
<div class="capability-text">
Learn about products, payments, shipping,
and return policies.
</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
<div class="capability-card">
<div class="capability-title">Smart Calculations</div>
<div class="capability-text">
Calculate order totals, discounts,
and shipping fees.
</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
<div class="capability-card">
<div class="capability-title">Live Conversion</div>
<div class="capability-text">
Convert currencies using available
exchange-rate data.
</div>
</div>
""",
            unsafe_allow_html=True,
        )


# ============================================================
# Display Chat History
# ============================================================

for message in st.session_state.chat_history:

    display_message(
        role=message["role"],
        content=message["content"],
    )


# ============================================================
# Handle Sidebar Question
# ============================================================

if "pending_question" in st.session_state:

    question = st.session_state.pop(
        "pending_question"
    )

    process_user_message(question)

    st.rerun()


# ============================================================
# Chat Input
# ============================================================

user_input = st.chat_input(
    "Ask LumaAssist anything about LumaCart..."
)


if user_input:

    process_user_message(user_input)

    st.rerun()