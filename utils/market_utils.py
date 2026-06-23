import time
import pytz

import datetime
from datetime import time as dt_time
import win32com.client as win32
from utils.logger import logger
import pandas as pd
import pickle

def wait_until_920():

    logger.info("Waiting until 9:20")
    print("Waiting until 920...")
    while True:

        now = datetime.datetime.now(
            pytz.timezone("Asia/Kolkata")
        ).time()
        if now >= dt_time(15, 18):
            return False

        if now >= dt_time(9, 30):
            return True

        time.sleep(30)

def get_previous_session_price(smart_api , token):
    today = datetime.date.today()

    from_date = today - datetime.timedelta(days=7)

    params = {
        "exchange": "NSE",
        "symboltoken": token,
        "interval": "FIFTEEN_MINUTE",
        "fromdate": from_date.strftime("%Y-%m-%d") + " 09:15",
        "todate": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d") + " 15:30"
    }

    candles = smart_api.getCandleData(params)

    if not candles or not candles.get("data"):
        return None

    data = candles["data"]

    # latest trading day only
    last_day = data[-1][0][:10]

    last_session = [
        c for c in data
        if c[0][:10] == last_day
    ]

    # 09:15 candle
    first_candle = last_session[0]

    # candle format:
    # [timestamp, open, high, low, close, volume]

    price_930 = float(first_candle[4])

    return price_930
def is_market_open(broker, symbol, token):

    try:

        ltp = broker.ltpData(
            exchange="NSE",
            tradingsymbol=symbol,
            symboltoken=token
        )

        if ltp.get("data"):
            print(
                f"Market open.{symbol} LTP: {ltp['data']['ltp']}"
            )

            return ltp['data']['ltp']

        return None

    except Exception as e:

        print(f"Market check failed: {e}")

        return False
def initialize_day(smart_api):
    cols = {
        ("NIFTY", "99926000"): "C",
        ("NIFTY MIDCAP 100", "99926011"): "D",
        ("NIFTY SMLCAP 100", "99926032"): "F"
    }
    VIX_TOKEN = 99926017
    VIX_SYMBOL = "INDIA VIX"
    VIX_COLUMN = "Z"
    excel = win32.Dispatch("Excel.Application")

    excel.Visible = False
    excel.DisplayAlerts = False

    wb = excel.Workbooks.Open(
        r"C:\Users\aditya\Desktop\projects\Trading_System\indicator_new.xlsx"
    )

    ws = wb.Worksheets("Sheet4")

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    yesterday_yahoo = yesterday.strftime("%Y-%m-%d")
    today_yahoo = today.strftime("%Y-%m-%d")

    # Find actual last used row in column A
    last_row = ws.Cells(ws.Rows.Count, 1).End(-4162).Row

    last_date = ws.Range(f"A{last_row}").Value

    if last_date:

        if isinstance(last_date, datetime.datetime):
            last_date = last_date.date()

        if last_date == today:

            print("Already existing")

            wb.Close(SaveChanges=False)
            excel.Quit()

            return
    
    first_blank_row = last_row + 1
    vix_ltp = is_market_open(smart_api , VIX_SYMBOL , VIX_TOKEN)
    time.sleep(2)
    print(f"First blank row: {first_blank_row}")
    cell = ws.Range(f"{VIX_COLUMN}{first_blank_row}")
    cell.Value = vix_ltp 
    cell.NumberFormat = "0.00"
    for symbol, token in cols.keys():

        col_no = cols[(symbol, token)]

        ltp = is_market_open(smart_api , symbol, token)

        time.sleep(2)
        open_price = get_previous_session_price(smart_api , token)
        print("open: " , open_price , " ltp: " , ltp)
        ret = (ltp - open_price) / open_price

        cell = ws.Range(
            f"{col_no}{first_blank_row}"
        )

        cell.Value = ret

        cell.NumberFormat = "0.00%"

    date_cell = ws.Range(
        f"A{first_blank_row}"
    )

    date_cell.Value = datetime.datetime.now()

    date_cell.NumberFormat = "DD-MM-YYYY"

    all_cols = (
        [chr(ord('A') + x) for x in range(1, 25)]
        + [f"A{chr(ord('A') + x)}" for x in range(2)]
    )

    for col in all_cols:

        current_cell = ws.Range(
            f"{col}{first_blank_row}"
        )

        if current_cell.Value is not None:
            continue

        prev_cell = ws.Range(
            f"{col}{first_blank_row - 1}"
        )

        if (
            isinstance(prev_cell.Formula, str)
            and prev_cell.Formula.startswith("=")
        ):
            # True Excel drag-down behaviour
            prev_cell.AutoFill(
                Destination=ws.Range(
                    f"{col}{first_blank_row - 1}:{col}{first_blank_row}"
                )
            )

    wb.Save()

    wb.Close()

    excel.Quit()
def model_predict():
    data = pd.read_excel("indicator_new.xlsx" , sheet_name="Sheet4" , skiprows=6)
    train_data  =  pd.read_csv("xg_train.csv").drop(["Unnamed: 0"] , axis = 1)
    data = data[train_data.columns].dropna().astype(train_data.dtypes).iloc[-1: , :]
    with open("model.pkl" , "rb") as f:
        model = pickle.load(f)
        prediction = model.predict_proba(data)
        print(prediction[0][1])
