
class Kline():


    def __init__(self):
        self.high = None
        self.open = None
        self.close = None
        self.low = None
        self.volume = None
        self.date_time = None

    def set_dict(self, data: dict):
        self.high = data.get("high")
        self.open = data.get("open")
        self.close = data.get("close")
        self.low = data.get("low")
        self.volume = data.get("volume")
        self.date_time = data.get("date_time")

    def get_dict(self):
        return {
            "high": self.high,
            "open": self.open,
            "low": self.low,
            "volume": self.volume,
            "close": self.close,
            "date_time": self.date_time
        }
