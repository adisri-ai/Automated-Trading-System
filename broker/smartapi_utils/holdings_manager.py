from utils.logger import logger


class HoldingsManager:

    def __init__(self, broker):

        self.broker = broker

        # Keeps active F&O / equity positions cached
        self.cached_holdings = list()

    def refresh_holdings(self):

        try:

            positions = self.broker.position()

            self.cached_holdings = list()

            if positions and positions.get("data"):

                for position in positions["data"]:
                    try:
                        if(position.get("exchange")!="NFO"): continue
                        net_qty = float(
                            position.get("netqty", 0)
                        )

                    except Exception:

                        net_qty = 0

                    # Active position exists
                    if net_qty != 0:

                        self.cached_holdings.append(
                            position
                        )

            logger.info(
                f"Positions refreshed: {self.cached_holdings}"
            )
            print(f"Positions refresherd: {self.cached_holdings}")

        except Exception as e:

            print(f"Positions refresh failed: {e}")

            logger.error(
                f"Positions refresh failed: {e}"
            )

    def has_holding(self, symbol):

        return symbol in self.cached_holdings