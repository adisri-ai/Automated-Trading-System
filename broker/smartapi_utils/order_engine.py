from utils.logger import logger
from config.settings import MAX_RETRY

class SmartApiOrders:

    def __init__(self, smart_api):
        self.smart_api = smart_api

    def place_order(self, params):

        retry = 0

        while retry < MAX_RETRY:
            try:
                order_id = self.smart_api.placeOrder(params)
                print(f"Order placed: {order_id}") 
                logger.info(f"Order placed: {order_id}")
                return order_id

            except Exception as e:
                retry += 1
                print(f"Order failed: {e}")
                logger.error(f"Order failed: {e}")

        raise Exception("Max retry exceeded")
