import streamlit as st
import threading
import os
import execution

from utils.market_utils import *

STOP_EVENT = threading.Event()
def run_trading_loop(
    api_key,
    client_code,
    pin,
    totp_secret
):

    try:

        print("Trading loop started")
        wait_status = wait_until_920()
        if not wait_status:
            print("Time over")
            return

        if STOP_EVENT.is_set():
            return
        os.environ["API_KEY"] = api_key
        os.environ["CLIENT_CODE"] = client_code
        os.environ["PIN"]  = pin
        os.environ["TOTP_SECRET"] = totp_secret
        execution.execution()
    except Exception as e:
        print(e)
        raise SystemExit
st.set_page_config(
    page_title="Nifty Calendar Spread",
    page_icon="📈",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
}

.status-card {
    padding: 20px;
    border-radius: 10px;
    background-color: #262730;
    margin-bottom: 15px;
}

.big-font {
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)
st.title(
    "Nifty Calendar Spread Trading System"
)
if "trading_thread" not in st.session_state:
    st.session_state.trading_thread = None

if "running" not in st.session_state:
    st.session_state.running = False
with st.sidebar:

    st.header("Broker Configuration")

    api_key = st.text_input(
        "API Key"
    )

    client_code = st.text_input(
        "Client Code"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    totp_secret = st.text_input(
        "TOTP Secret",
        type="password"
    )
if st.button(
    "Start Trading System",
    type="primary"
):

    if st.session_state.running:

        st.warning(
            "System already running"
        )

    else:

        STOP_EVENT.clear()

        trading_thread = threading.Thread(
            target=run_trading_loop,
            args=(
                api_key,
                client_code,
                pin,
                totp_secret
            ),
            daemon=True
        )

        trading_thread.start()

        st.session_state.trading_thread = (
            trading_thread
        )

        st.session_state.running = True

        st.success(
            "Trading system started"
        )
if st.button(
    "Stop Trading System"
):

    if not st.session_state.running:

        st.warning(
            "System not running"
        )

    else:

        STOP_EVENT.set()

        st.session_state.running = False

        st.success(
            "Stop signal sent"
        )
st.header("Status")

if st.session_state.running:

    st.success(
        "RUNNING"
    )

else:

    st.error(
        "STOPPED"
    )
