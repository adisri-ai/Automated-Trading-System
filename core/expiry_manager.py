from datetime import datetime
from datetime import timedelta

import pytz


class ExpiryManager:

    def __init__(self):

        self.tz = pytz.timezone("Asia/Kolkata")

    def get_now(self):

        return datetime.now(self.tz)

    def get_monthly_expiry(self):

        """
        Placeholder.
        Replace later using actual NSE expiry calendar.
        """

        now = self.get_now()

        # temporary approximation
        # last Thursday logic

        expiry = now

        while expiry.weekday() != 3:
            expiry += timedelta(days=1)

        return expiry.date()

    def is_expiry_day(self):

        return (
            self.get_now().date()
            ==
            self.get_monthly_expiry()
        )

    def is_one_day_before_expiry(self):

        return (
            self.get_now().date()
            ==
            self.get_monthly_expiry() - timedelta(days=1)
        )