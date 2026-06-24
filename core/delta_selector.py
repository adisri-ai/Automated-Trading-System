# delta_selector.py
import time


class DeltaSelector:
    def __init__(self , broker):
        self.broker = broker
    @staticmethod
    def _best_by_target(
        candidates,
        target_delta
    ):

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda x: (
                abs(
                    float(x["delta"])
                    - target_delta
                ),
                -float(x["delta"]),
            )
        )

    @staticmethod
    def select_next_month_buy(
        chain
    ):

        candidates = []

        for option in chain:

            if (
                option["option_type"]
                != "CE"
            ):
                continue

            if (
                option["strike"]
                % 500 != 0
            ):
                continue

            candidates.append(
                option
            )

        return DeltaSelector._best_by_target(
            candidates,
            0.6
        )

    @staticmethod
    def select_current_month_sell(
        chain
    ):

        candidates = []

        for option in chain:

            if (
                option["option_type"]
                != "CE"
            ):
                continue

            if (
                option["strike"]
                % 100 != 0
            ):
                continue

            candidates.append(
                option
            )

        return DeltaSelector._best_by_target(
            candidates,
            0.4
        )

    def select_sell_adjustment_option(
        self,
        chain,
        current_option_price,
        market_data,
        flag = False,
    ):

        candidates = []

        for option in chain:

            if (
                option["option_type"]
                != "CE"
            ):
                continue

            if (
                float(option["delta"])
                < 0.4
            ):
                continue

            candidates.append(
                option
            )

        candidates.sort(
            key=lambda x: (
                abs(
                    float(x["delta"])
                    - 0.4
                ),
                -float(x["delta"]),
            )
        )

        for option in candidates:

            response = self.broker.ltpData(
                exchange="NFO",
                tradingsymbol=option["symbol"],
                symboltoken=option["token"]
            )

            data = response.get("data")

            if not data:
                continue

            ltp_value = float(
                data["ltp"]
            )

            if ltp_value is None:
                time.sleep(1)
                continue

            return option

        print(
            "Could not find an option during sell redjustemnt"
        )

        return None