from typing import Union

from kraken_api.mock import KrakenMockAPI
from kraken_api.websocket import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    kraken_api: Union[KrakenWebsocketAPI, KrakenMockAPI],
):
    """
    It does 2 things:
    1. Reads trades from the Kraken API
    2. Pushes them to a Kafka topic.

    Args:
        kafka_broker_address: str
        kafka_topic: str
        kraken_api: Union[KrakenWebsocketAPI, KrakenMockAPI]
    """
    logger.info('Start the trades service')

    # Initialize the Quix Streams application.
    # This calss handles all the low-level details to connect to Kafka.
    app = Application(broker_address=kafka_broker_address, consumer_group='example')

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic, value_serializer='json')

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            trades = kraken_api.get_trades()

            for trade in trades:
                # Serialize the trade (i.e. event) as bytes using the defined Topic
                message = topic.serialize(
                    key=trade.pair,
                    value=trade.to_dict(),
                )

                # Push the serialized trade (i.e. message) to a Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Pushed trade to Kafka: {trade}')


if __name__ == '__main__':
    from config import config

    kraken_api = KrakenWebsocketAPI(pairs=config.pairs)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        kraken_api=kraken_api,
    )
