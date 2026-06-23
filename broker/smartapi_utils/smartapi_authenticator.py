from SmartApi import SmartConnect
import pyotp
import config.settings as cf
class SmartApiClient:

    def __init__(self):
        print("Connecting api key")
        self.smart = SmartConnect(api_key=cf.API_KEY)
        print("Api key connected")
        self.session = None
        self.authToken_trading, self.feedToken_trading, self.refreshToken_trading = None, None, None

    def login(self):
        global authToken_trading, feedToken_trading, refreshToken_trading
        try:
            token = cf.TOTP_SECRET
            username = cf.CLIENT_CODE
            pwd = cf.PASSWORD
            totp = pyotp.TOTP(token).now()
            data = self.smart.generateSession(username, pwd, totp)
            if not data['status']:
                print("Trading login failed")
                return False
            authToken_trading = data['data']['jwtToken']
            refreshToken_trading = data['data']['refreshToken']
            feedToken_trading = self.smart.getfeedToken()
            print("Trading API login successful")
            return self.smart
        except Exception as e:
            print("Trading login error:", e)
            return False
    def terminateSession(self): 
        self.smart.terminateSession(cf.CLIENT_CODE)