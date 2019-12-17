

class UserRequest:
    """
    Stores the user request to refer later in the program.
    """
    def __init__(self,side, contract_size, time_interval,
                 take_profit, stop_loss):
        self.side = str.title(side)
        self.contract_size = contract_size
        self.time_interval = time_interval
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def get_side(self):
        return self.side

    def get_tp(self):
        return self.take_profit