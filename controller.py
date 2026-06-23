import time
import datetime
import pytz
import sys
import logging
def wait_until_920():
    global status
    print("Waiting until 920....")
    while True:
        now = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).time()
        if now >= datetime.time(15, 18):
            print("Too late to start.")
            status = "OVER"
            return
        if now < datetime.time(9 , 20):
            time.sleep(30)
        else:
            return
def shutdown():
    try:
        print("Initating shutdown...")
        save_positions_to_txt()
        sws.close_connection()
        logout_trading()
        time.sleep(5)
        logout_historic()
        sys.exit()
        return
    except Exception as e:
        logging.warning(f"Shutdown error: {e}")
        sys.exit()
        return
def is_market_open():
    global TOKENS
    try:
        token = "NIFTYBEES-EQ"
        ltp = smartApi_trading.ltpData(exchange="NSE", tradingsymbol=token, symboltoken=TOKENS[token])
        if(ltp.get("data") is not None):
            print(f"ltp fetched for {token} : {ltp['data']['ltp']}")
        else: 
            return False
        return True
    except:
        return False