from kraken_api.base import TradesAPI
from kraken_api.mock import KrakenMockAPI
from kraken_api.rest import KrakenRestAPI
from kraken_api.websocket import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    trades_api: TradesAPI,
):
    """
    It does 2 things:
    1. Reads trades from the Kraken API
    2. Pushes them to a Kafka topic.

    Args:
        kafka_broker_address: str
        kafka_topic: str
        trades_api: TradesAPI with 2 methods: get_trades and is_done
    """
    logger.info('Start the trades service')

    # Initialize the Quix Streams application.
    # This calss handles all the low-level details to connect to Kafka.
    app = Application(broker_address=kafka_broker_address, consumer_group='example')

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic, value_serializer='json')

    # Create a Producer instance
    with app.get_producer() as producer:
        while not trades_api.is_done():
            trades = trades_api.get_trades()

            for trade in trades:
                # Serialize the trade (i.e. event) as bytes using the defined Topic
                message = topic.serialize(
                    key=trade.pair.replace('/', '-'),
                    value=trade.to_dict(),
                )

                # Push the serialized trade (i.e. message) to a Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Pushed trade to Kafka: {trade}')


if __name__ == '__main__':
    from config import config

    # Initialize the Kraken API depending on the data source
    if config.data_source == 'live':
        kraken_api = KrakenWebsocketAPI(pairs=config.pairs)
    elif config.data_source == 'historical':
        kraken_api = KrakenRestAPI(pairs=config.pairs, last_n_days=config.last_n_days)

        # # TODO: remove this once we are done debugging the KrakenRestAPISinglePair
        # from kraken_api.rest import KrakenRestAPISinglePair
        # kraken_api = KrakenRestAPISinglePair(
        #     pair=config.pairs[0],
        #     last_n_days=config.last_n_days,
        # )

    elif config.data_source == 'test':
        kraken_api = KrakenMockAPI(pairs=config.pairs)
    else:
        raise ValueError(f'Invalid data source: {config.data_source}')

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        trades_api=kraken_api,
    )
