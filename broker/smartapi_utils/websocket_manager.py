# websocket_manager.py
import threading
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import time
import datetime
from utils.logger import logger
from config.settings import (
    NIFTY_FUTURE_SYMBOL,
    NIFTY_FUTURE_TOKEN
)
import pytz
import sys
from strategy.nifty_calendar_strategy import NiftyCalendarStrategy
class WebSocketManager:

    def __init__(
        self,
        auth_token,
        api_key,
        client_code,
        feed_token,
        strategy :  NiftyCalendarStrategy
    ):

        self.strategy = strategy

        self.lock = threading.RLock()

        self.market_data = {}

        self.subscribed_tokens = set()

        self.sws = SmartWebSocketV2(
            auth_token,
            api_key,
            client_code,
            feed_token
        )

        return

    def subscribe_token(
        self,
        token
    ):

        token = str(token)

        if token in self.subscribed_tokens:
            return

        self.subscribed_tokens.add(token)

        try:

            if (
                not hasattr(self.sws, "wsapp")
                or self.sws.wsapp is None
            ):

                logger.info(
                    f"Token queued until websocket opens: {token}"
                )

                return

            self.sws.subscribe(
                "dynamic_tokens",
                1,
                [{
                    "exchangeType": 2,
                    "tokens": [token]
                }]
            )
        except Exception as e:
            print(f"Token subscribe failed: {e}")

    def on_data(self, wsapp, message):

        with self.lock:

            try:

                if (
                    datetime.datetime.now(
                        pytz.timezone(
                            'Asia/Kolkata'
                        )
                    ).time()
                    >= datetime.time(15, 18)
                ):

                    print(
                        "Time over. Disconnecting.."
                    )

                    self.close()

                    return

                token = str(
                    message["token"]
                )

                ltp = (
                    message[
                        "last_traded_price"
                    ] / 100
                )

                self.market_data[token] = ltp

                self.strategy.evaluate_tick(
                    token,
                    ltp,
                    self.market_data
                )

                return

            except Exception as e:

                logger.error(
                    f"on_data error: {e}"
                )

                return

    def on_open(self, wsapp):

        logger.info(
            "WebSocket Opened"
        )

        tokens = list(self.subscribed_tokens)

        self.sws.subscribe(
            "abc123",
            1,
            [{
                "exchangeType": 2,
                "tokens": tokens
            }]
        )

        return

    def on_error(
        self,
        wsapp,
        error
    ):

        logger.error(error)

        return

    def on_close(
        self,
        wsapp
    ):

        logger.info(
            "WebSocket Closed"
        )
        raise SystemExit

        return

    def connect(self):

        self.sws.on_data = self.on_data

        self.sws.on_open = self.on_open

        self.sws.on_error = self.on_error

        self.sws.on_close = self.on_close
        self.sws.on_error = self.on_error

        self.sws.connect()
        return
    def on_error(self, wsapp, error):

        logger.error(f"WebSocket error: {error}")

        print(f"WebSocket error: {error}")

        print("Internet/WebSocket connection lost. Exiting system.")

        try:
            self.close()
        except:
            pass

        sys.exit()
    def close(self):

        try:

            self.sws.close_connection()

            return

        except Exception as e:

            logger.error(
                f"WebSocket close failed: {e}"
            )

            return