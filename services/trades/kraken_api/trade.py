from datetime import datetime

from pydantic import BaseModel


class Trade(BaseModel):
    """
    A trade from the Kraken API.
    """

    pair: str
    price: float
    volume: float
    timestamp: datetime
    timestamp_ms: int

    # # TODO: let Pydantic do the initialization of timestamp_ms from timestamp
    # @field_validator('timestamp_ms', mode="after")
    # def compute_timestamp_ms(cls, v, values):
    #     """
    #     Converts the timestamp to milliseconds.
    #     This function is called automatically by Pydantic when I create a Trade a object
    #     """
    #     # Convert datetime to milliseconds timestamp
    #     return int(values.data['timestamp'].timestamp() * 1000)

    def to_dict(self) -> dict:
        # pydantic method to convert the model to a dict
        return self.model_dump_json()

        # alternatively, if you prefer not to serialize all the fields:
        # return {
        #     "pair": self.pair,
        #     "price": self.price,
        #     "volume": self.volume,
        #     "timestamp_ms": self.timestamp_ms,
        #     "timestamp": self.timestamp,
        # }
