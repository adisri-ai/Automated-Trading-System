import sys

from utils.logger import logger


class RuntimeManager:

    def __init__(
        self,
        websocket_manager,
        repository,
        strategy,
        broker
    ):

        self.websocket_manager = websocket_manager

        self.repository = repository
        self.strategy = strategy

        self.broker = broker

    def shutdown(self):

        logger.info("Initiating shutdown")
        print("Initiating Shutdown")
        try:

            self.repository.save(
                self.strategy.serialize()
            )

        except Exception as e:
            print(f"Save failed: {e}")
            logger.error(f"Save failed: {e}")

        try:
            self.websocket_manager.close()
        except Exception as e:
            print(f"Websocket close failed: {e}")
            logger.error(f"WebSocket close failed: {e}")

        try:
            self.broker.terminateSession("CLIENT_CODE")
        except Exception as e:
            print(f"Logout Failed: {e}")
            logger.error(f"Logout failed: {e}")

        sys.exit()
