class PnlCalculator:

    @staticmethod
    def calculate(position, current_ltp):

        if position.side == "BUY":
            return (
                current_ltp - position.entry_price
            ) * position.quantity

        return (
            position.entry_price - current_ltp
        ) * position.quantity