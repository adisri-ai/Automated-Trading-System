
# greeks_engine.py

import pandas as pd
import requests

from config.settings import (
    CURRENT_MONTH_EXPIRY,
    NEXT_MONTH_EXPIRY,
    FAR_MONTH_EXPIRY
)


class GreeksEngine:

    MASTER_URL = (
        "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    )

    def __init__(self, broker):

        self.broker = broker

        self.master_df = None

        self.load_master_contract()
    def load_master_contract(self):

        response = requests.get(
            self.MASTER_URL
        )

        data = response.json()

        self.master_df = pd.DataFrame(data)

    def get_current_expiry(self):

        return CURRENT_MONTH_EXPIRY

    def get_next_expiry(self):

        return NEXT_MONTH_EXPIRY

    def get_far_expiry(self):

        return FAR_MONTH_EXPIRY

    def get_expiry_by_type(
        self,
        expiry_type
    ):

        if expiry_type == "CURRENT":
            return self.get_current_expiry()

        if expiry_type == "NEXT":
            return self.get_next_expiry()

        if expiry_type == "FAR":
            return self.get_far_expiry()

        raise ValueError(
            f"Invalid expiry type: {expiry_type}"
        )

    def get_token_from_symbol(
        self,
        symbol
    ):

        try:

            option_scrip = self.master_df[
                (
                    self.master_df["symbol"]
                    == symbol
                )
                &
                (
                    self.master_df["exch_seg"]
                    == "NFO"
                )
            ]

            if option_scrip.empty:
                return None

            return str(
                option_scrip.iloc[0]["token"]
            )

        except Exception as e:
            print(f"Error while getting token for symbol {symbol}  : {e}")
            return None

    def get_ltp(
        self,
        symbol,
        token
    ):

        try:

            response = self.broker.ltpData(
                exchange="NFO",
                tradingsymbol=symbol,
                symboltoken=token
            )

            if (
                response
                and response.get("data")
            ):

                return float(
                    response["data"]["ltp"]
                )

        except Exception as e:
            print("Error while fetcnhing ltp : {e}")
            return

        return 0

    def get_option_chain(
        self,
        underlying="NIFTY",
        expiry_type=None
    ):

        expiry = None

        if expiry_type is not None:

            expiry = self.get_expiry_by_type(
                expiry_type
            )
        greek_params = {
            "name" : underlying,
            "expirydate" : expiry
        }
        response = self.broker.optionGreek(
            greek_params
        )

        if (
            not response
            or not response.get("status")
            or "data" not in response
        ):
            print("Got null response while fetching option greeks")
            print(f"Response {response}")
            return []
        chain = []

        for option in response["data"]:

            try:

                strike = int(
                    float(
                        option["strikePrice"]
                    )
                )

                symbol = (
                    f"{option['name']}"
                    f"{option['expiry'][:-4]}"
                    f"{option['expiry'][-2:]}"
                    f"{strike}"
                    f"{option['optionType']}"
                )

                token = self.get_token_from_symbol(
                    symbol
                )

                if token is None:
                    continue

                transformed = {

                    "symbol": symbol,

                    "token": token,

                    "expiry": option[
                        "expiry"
                    ],

                    "strike": strike,

                    "option_type": option[
                        "optionType"
                    ],

                    "delta": abs(
                        float(
                            option["delta"]
                        )
                    ),

                    "gamma": float(
                        option["gamma"]
                    ),

                    "theta": float(
                        option["theta"]
                    ),

                    "vega": float(
                        option["vega"]
                    ),

                    "iv": float(
                        option[
                            "impliedVolatility"
                        ]
                    ),

                    "volume": float(
                        option.get(
                            "tradeVolume",
                            0
                        )
                    )
                }

                chain.append(
                    transformed
                )

            except Exception as e:
                print(f"Option parse failed : {e}")
                continue

        return chain