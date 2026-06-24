import os
import json
from config.settings import POSITIONS_FILE

class TxtRepository:

    def save(self, data):

        with open(POSITIONS_FILE, "w") as f:
            json.dump(data, f, default=str)

    def load(self):

        if not os.path.exists(POSITIONS_FILE):
            return None

        with open(POSITIONS_FILE, "r") as f:

            content = f.read().strip()

            if not content:
                return None

            return json.loads(content)
