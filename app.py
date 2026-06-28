import streamlit as st
import threading
import time
import datetime
import pytz
import sys
import os 

from broker.smartapi.smartapi_client import SmartApiClient
from broker.smartapi.smartapi_orders import SmartApiOrders

from execution.expiry_manager import ExpiryManager
from execution.order_manager import OrderManager
from execution.fund_manager import FundManager
from execution.holdings_manager import HoldingsManager
import pandas as pd

from persistence.txt_repository import TxtRepository

from market.greeks_engine import GreeksEngine
from market.websocket_manager import WebSocketManager

from strategy.engines.pnl_engine import PnlEngine
from strategy.nifty_calendar_strategy import (
    NiftyCalendarStrategy
)

from strategy.selectors.delta_selector import DeltaSelector

from core.runtime_manager import RuntimeManager

from utils.market_utils import * 
from utils.streamlit_logger import LOG_BUFFER

from streamlit_autorefresh import st_autorefresh
# ============================================
# GLOBAL CONTROL FLAG
# ============================================

STOP_EVENT = threading.Event()
st.set_page_config(
        page_title="Nifty Calendar Strategy",
        layout="wide"
    )

# ============================================
# TRADING THREAD
# ============================================
page = st.sidebar.radio(

    "",

    [

        "📈 Trading Dashboard",

        "⚙️ Configuration",

        "📊 Current Positions",

        "📖 Strategy Documentation"

    ]
)
if page == "⚙️ Configuration":

    st.title("⚙️ Broker Configuration")

    st.write(
        "Configure your Angel One credentials."
    )

    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    if "client_code" not in st.session_state:
        st.session_state.client_code = ""

    if "pin" not in st.session_state:
        st.session_state.pin = ""

    if "totp_secret" not in st.session_state:
        st.session_state.totp_secret = ""

    col1, col2 = st.columns(2)

    with col1:

        st.session_state.api_key = st.text_input(
            "API Key",
            value=st.session_state.api_key
        )

        st.session_state.client_code = st.text_input(
            "Client Code",
            value=st.session_state.client_code
        )

    with col2:

        st.session_state.pin = st.text_input(
            "PIN",
            value=st.session_state.pin,
            type="password"
        )

        st.session_state.totp_secret = st.text_input(
            "TOTP Secret",
            value=st.session_state.totp_secret,
            type="password"
        )

    st.divider()

    st.subheader("Strategy Parameters")

    st.session_state.threshold = st.number_input(
        "Current Month Profit Threshold",
        value=4000
    )

    st.session_state.qty = st.number_input(
        "Lot Quantity",
        value=1
    )

    if st.button("💾 Save Configuration"):

        os.environ["API_KEY"] = st.session_state.api_key
        os.environ["CLIENT_CODE"] = st.session_state.client_code
        os.environ["PIN"] = st.session_state.pin
        os.environ["TOTP_SECRET"] = st.session_state.totp_secret
        os.environ["CURRENT_MONTH_THRESHOLD"] = str(
            st.session_state.threshold
        )
        os.environ["LOT_QTY"] = str(
            st.session_state.qty
        )

        st.success("Configuration saved.")
if page=="📈 Trading Dashboard":
    def run_trading_loop(
        api_key,
        client_code,
        pin,
        totp_secret
    ):

        runtime_manager = None

        try:

            print("Trading loop started")

            wait_status = wait_until_920()

            if not wait_status:
                print("Time over")
                return

            if STOP_EVENT.is_set():
                return

            client = SmartApiClient(
                api_key=api_key,
                client_code=client_code,
                pin=pin,
                totp_secret=totp_secret
            )

            smart = client.login()

            if not is_market_open(
                smart,
                "NIFTY",
                "99926000"
            ):
                print("Market not open")
                return

            repository = TxtRepository()

            holdings_manager = HoldingsManager(
                smart
            )

            holdings_manager.refresh_holdings()

            fund_manager = FundManager(
                smart
            )

            fund_manager.refresh_balance()

            broker_orders = SmartApiOrders(
                smart
            )

            greeks_engine = GreeksEngine(
                smart
            )

            delta_selector = DeltaSelector()

            pnl_engine = PnlEngine()

            expiry_manager = ExpiryManager()

            order_manager = OrderManager(
                broker_orders,
                repository,
                holdings_manager,
                fund_manager
            )

            strategy = NiftyCalendarStrategy(
                greeks_engine=greeks_engine,
                order_manager=order_manager,
                repository=repository,
                option_selector=delta_selector,
                pnl_engine=pnl_engine,
                fund_manager=fund_manager
            )

            order_manager.strategy = strategy

            websocket_manager = WebSocketManager(
                auth_token=client.session['data']['jwtToken'],
                api_key=api_key,
                client_code=client_code,
                feed_token=smart.getfeedToken(),
                strategy=strategy
            )

            strategy.websocket_manager = (
                websocket_manager
            )

            strategy.initialize()

            runtime_manager = RuntimeManager(
                websocket_manager,
                repository,
                strategy,
                smart
            )

            websocket_manager.connect()

            while not STOP_EVENT.is_set():

                if STOP_EVENT.is_set():

                    print(
                        "Manual stop requested"
                    )

                    runtime_manager.shutdown()

                    break

                if (
                    datetime.datetime.now(
                        pytz.timezone(
                            "Asia/Kolkata"
                        )
                    ).time()
                    >= datetime.time(15, 18)
                ):

                    print(
                        "Trading session over"
                    )

                    runtime_manager.shutdown()

                    break

                time.sleep(1)

        except Exception as e:

            print(
                f"Fatal Error : {e}"
            )

            if runtime_manager:

                try:
                    runtime_manager.shutdown()
                except:
                    pass

    st.title(
        " 📈 Trading Dashboard"
    )
    if "trading_thread" not in st.session_state:
        st.session_state.trading_thread = None

    if "running" not in st.session_state:
        st.session_state.running = False
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
                    st.session_state.api_key,
                    st.session_state.client_code,
                    st.session_state.pin,
                    st.session_state.totp_secret
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
    st.header("System Status")
    st.divider()

    st.subheader("Live Logs")

    log_box = st.empty()

    logs = "\n".join(LOG_BUFFER)

    log_box.text_area(
        "",
        logs,
        height=450
    )
    if st.session_state.running:


        st.success(
            "RUNNING"
        )

    else:

        st.error(
            "STOPPED"
        )
if page=="📖 Strategy Documentation": 
    st.title(
        "Nifty Calendar Spread Strategy"
    )
    st.header("Overview")

    st.write("""

    This strategy implements a Delta-based Nifty Calendar Spread.

    The system simultaneously

    • Buys a Next Month Call

    • Sells a Current Month Call

    The objective is to benefit from time decay in the near-month option while maintaining a hedge using the next-month option.

    """)
    st.header("Entry")

    st.markdown("""

    - Buy Next Month CE
    - Delta ≈ 0.6
    - Strike multiple of 500

    - Sell Current Month CE
    - Delta ≈ 0.40
    - Strike multiple of 100

    """)
    st.header("Adjustment")

    st.markdown("""

    Whenever:

    • Delta ≥ 0.65

    OR

    • Profit ≥ ₹4000

    the short option is squared off and replaced with another current-month CE whose premium is at least ₹25 higher and whose delta is closest to 0.40.

    """)
    st.header("Expiry Management")

    st.markdown("""

    One day before expiry:

    • If profit target achieved

    OR

    • Delta exceeds threshold

    the calendar spread is rolled over into the next expiry.

    """)
    st.header("Risk Controls")

    st.markdown("""

    ✔ Position recovery from broker

    ✔ Automatic monitoring of order completion

    ✔ Duplicate order prevention

    ✔ Fund availability checks

    ✔ WebSocket-based live pricing

    ✔ Broker synchronization after restart

    ✔ Persistent repository storage

    """)
    st.header("Architecture")

    st.code("""

    Streamlit UI
        │
        ▼
    Execution Engine
        │
        ▼
    Strategy
        │
        ├── Greeks Engine
        ├── Order Manager
        ├── PnL Engine
        ├── Delta Selector
        ├── Holdings Manager
        └── WebSocket Manager

    """)
if page == "📊 Current Positions":

    st.title("📊 Current Positions")

    st.write(
        "Live strategy positions."
    )

    repository = TxtRepository()

    data = repository.load()

    if not data:

        st.info(
            "No positions available."
        )

    else:

        positions = data.get(
            "positions",
            {}
        )

        rows = []

        for name, pos in positions.items():

            if pos is None:
                continue

            rows.append({

                "Leg": name,

                "Symbol": pos.get("symbol"),

                "Side": pos.get("side"),

                "Qty": pos.get("qty"),

                "Entry Price": pos.get("entry_price"),

                "Token": pos.get("token"),

                "Delta": pos.get("delta"),

                "Gamma": pos.get("gamma"),

                "Theta": pos.get("theta"),

                "Vega": pos.get("vega"),

                "IV": pos.get("iv")

            })

        if rows:

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True
            )

        else:

            st.info(
                "No active positions."
            )
