import threading
import time
import math
from utils.logger import logger


class OrderManager:

    def __init__(
        self,
        broker_orders,
        repository,
        positions_manager,
        fund_manager,
        strategy = None
    ):

        self.broker_orders = broker_orders

        self.repository = repository

        self.positions_manager = positions_manager

        self.fund_manager = fund_manager

        self.strategy = strategy

        self.lock = threading.RLock()

        self.pending_orders = False

        self.monitor_threads = {}

        self.broker = self.broker_orders.smart_api
    def wait_for_orders(self, timeout=300):

        start = time.time()

        while time.time() - start < timeout:

            with self.lock:

                if not self.pending_orders:
                    return True

            time.sleep(1)
        return False
    def buy(
        self,
        symbol,
        token,
        qty,
        price=None
    ):

        with self.lock:

            if self.pending_orders:

                print(
                    f"Pending order exists: {symbol}"
                )

                logger.info(
                    f"Pending order exists: {symbol}"
                )

                return None

            # refresh cached positions

            self.pending_orders = True

            params = {
                "variety": "NORMAL",
                "tradingsymbol": symbol,
                "symboltoken": token,
                "transactiontype": "BUY",
                "exchange": "NFO",
                "ordertype": "LIMIT",
                "producttype": "CARRYFORWARD",
                "duration": "DAY",
                "quantity": qty
            }

            for attempt in range(5):

                try:

                    ltp_response = self.broker.ltpData(
                        exchange="NFO",
                        tradingsymbol=symbol,
                        symboltoken=token
                    )

                    if not ltp_response.get("data"):

                        time.sleep(1)

                        continue

                    ltp = float(
                        ltp_response["data"]["ltp"]
                    )

                    time.sleep(1)

                except Exception as e:

                    logger.error(
                        f"LTP fetch failed for "
                        f"{symbol}: {e}"
                    )

                    time.sleep(1)

                    continue

                order_price = round(
                    ltp * 1.01,
                    2
                )
                order_price = round(math.ceil(order_price/0.05)*0.05 , 2)
                params["price"] = order_price
                try:

                    order_id = (
                        self.broker_orders.place_order(
                            params
                        )
                    )

                except Exception as e:
                    logger.error(
                        f"Place order failed: {e}"
                    )
                    orders = (
                        self.broker_orders
                        .smart_api
                        .orderBook()
                    )

                    for order in orders.get("data", []):

                        if (
                            order.get("tradingsymbol") == symbol
                            and
                            order.get("transactiontype") == "BUY"
                            and
                            int(order.get("quantity", 0)) == qty
                            and
                            order.get("status", "").lower()
                            in [
                                "open",
                                "trigger pending",
                                "complete"
                            ]
                        ):

                            recovered_order_id = order.get(
                                "orderid"
                            )

                            logger.info(
                                f"Recovered existing BUY order: "
                                f"{recovered_order_id}"
                            )

                            self.strategy.on_order_placed(
                                symbol=symbol,
                                side="BUY",
                                order_id=recovered_order_id
                            )

                            self.repository.save(
                                self.strategy.serialize()
                            )

                            self.start_monitoring(
                                symbol,
                                recovered_order_id,
                                True
                            )

                            return recovered_order_id

                    time.sleep(5)

                    continue

                if not order_id:

                    logger.warning(
                        f"BUY order failed (Attempt {attempt + 1}) for {symbol}"
                    )

                    time.sleep(60)

                    continue

                self.strategy.on_order_placed(
                    symbol=symbol,
                    side="BUY",
                    order_id=order_id
                )

                self.repository.save(
                    self.strategy.serialize()
                )

                self.start_monitoring(
                    symbol,
                    order_id,
                    True
                )

                return order_id

            self.pending_orders = False

            logger.error(
                f"BUY failed after retries: {symbol}"
            )

            return None

    def sell(
        self,
        symbol,
        token,
        qty
    ):

        with self.lock:

            if self.pending_orders:

                logger.info(
                    f"Pending order exists: {symbol}"
                )

                return None

            # refresh cached positions

            self.pending_orders = True

            params = {
                "variety": "NORMAL",
                "tradingsymbol": symbol,
                "symboltoken": token,
                "transactiontype": "SELL",
                "exchange": "NFO",
                "ordertype": "LIMIT",
                "producttype": "CARRYFORWARD",
                "duration": "DAY",
                "quantity": qty
            }

            for attempt in range(5):

                try:

                    ltp_response = self.broker.ltpData(
                        exchange="NFO",
                        tradingsymbol=symbol,
                        symboltoken=token
                    )

                    if not ltp_response.get("data"):

                        time.sleep(1)

                        continue

                    ltp = float(
                        ltp_response["data"]["ltp"]
                    )

                    time.sleep(1)

                except Exception as e:

                    logger.error(
                        f"LTP fetch failed for "
                        f"{symbol}: {e}"
                    )

                    time.sleep(1)

                    continue

                order_price = round(
                    ltp * 0.99,
                    2
                )
                order_price = round(math.floor(order_price/0.05)*0.05 , 2)
                params["price"] = order_price

                try:

                    order_id = (
                        self.broker_orders.place_order(
                            params
                        )
                    )

                except Exception as e:

                    logger.error(
                        f"Place order failed: {e}"
                    )
                    orders = (
                        self.broker_orders
                        .smart_api
                        .orderBook()
                    )

                    for order in orders.get("data", []):

                        if (
                            order.get("tradingsymbol") == symbol
                            and
                            order.get("transactiontype") == "BUY"
                            and
                            int(order.get("quantity", 0)) == qty
                            and
                            order.get("status", "").lower()
                            in [
                                "open",
                                "trigger pending",
                                "complete"
                            ]
                        ):

                            recovered_order_id = order.get(
                                "orderid"
                            )

                            logger.info(
                                f"Recovered existing BUY order: "
                                f"{recovered_order_id}"
                            )

                            self.strategy.on_order_placed(
                                symbol=symbol,
                                side="BUY",
                                order_id=recovered_order_id
                            )

                            self.repository.save(
                                self.strategy.serialize()
                            )

                            self.start_monitoring(
                                symbol,
                                recovered_order_id,
                                True
                            )

                            return recovered_order_id
                    time.sleep(5)

                    continue

                if not order_id:

                    logger.warning(
                        f"SELL order failed "
                        f"(Attempt {attempt + 1}) "
                        f"for {symbol}"
                    )

                    time.sleep(60)

                    continue

                self.strategy.on_order_placed(
                    symbol=symbol,
                    side="SELL",
                    order_id=order_id
                )

                self.repository.save(
                    self.strategy.serialize()
                )

                self.start_monitoring(
                    symbol,
                    order_id,
                    False
                )

                return order_id

            self.pending_orders = False

            logger.error(
                f"SELL failed after retries: {symbol}"
            )

            return None

    def start_monitoring(
        self,
        symbol,
        order_id,
        is_buy
    ):

        thread = threading.Thread(
            target=self.monitor_order,
            args=(
                symbol,
                order_id,
                is_buy
            ),
            daemon=True
        )

        self.monitor_threads[
            order_id
        ] = thread

        thread.start()

    def monitor_order(
        self,
        symbol,
        order_id,
        is_buy
    ):

        start = time.time()

        while time.time() - start < 300:

            try:

                orders = (
                    self.broker_orders
                    .smart_api
                    .orderBook()
                )

                for order in orders.get(
                    "data",
                    []
                ):
                    status = order["status"].lower()

                    if (order["orderid"]== order_id and status in [
                        "rejected",
                        "cancelled",
                        "expired"
                    ]):

                        logger.error(
                            f"Order failed: {symbol} | {status}"
                        )

                        with self.lock:

                            self.pending_orders = False

                        return
                    if (
                        order["orderid"] == order_id
                        and
                        order["status"].lower()
                        == "complete"
                    ):

                        logger.info(
                            f"Order completed: "
                            f"{symbol}"
                        )

                        print(
                            f"Order completed: "
                            f"{symbol}"
                        )

                        # refresh cached positions

                        self.repository.save(
                            self.strategy.serialize()
                        )

                        with self.lock:

                            self.pending_orders = False

                        if is_buy:

                            self.strategy.on_order_complete(
                                symbol=symbol,
                                side="BUY",
                                average_price=float(
                                    order[
                                        "averageprice"
                                    ]
                                )
                            )

                        else:

                            self.strategy.on_order_complete(
                                symbol=symbol,
                                side="SELL",
                                average_price=float(
                                    order[
                                        "averageprice"
                                    ]
                                )
                            )

                        return

                time.sleep(5)

            except Exception as e:

                logger.error(
                    f"Monitor failed: {e}"
                )

                time.sleep(5)

        with self.lock:
            time.sleep(2)
            self.pending_orders = False
            self.positions_manager.refresh_positions()

            self.fund_manager.refresh_balance()

        logger.error(
            f"Monitor timeout: {symbol}"
        )