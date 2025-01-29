import asyncio
import os
import threading
import logging
from fastapi import FastAPI
from src.consumer import KafkaConsumerService
from src.extractor import MongoSummaryService, SQLConnectorService
from src.producer import KafkaProducerService

# # TODO:
LIMIT = None

# Configure logging
logging.basicConfig(level=logging.INFO, format=f"[%(asctime)s] %(levelname)s - (%(filename)s:%(lineno)d) - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI()

# Initilize Procuer, Consumer and Extractor tasks
producer_thread = None
consumer_task = None
extractor_task = None

# Kafka and MongoDB configurations
KAFKA_TOPIC = 'my_topic'
KAFKA_BROKERS = ['localhost:9092'] # Change these!
MONGO_URI = 'mongodb://localhost:27017/' #cHANGE THESE! 
MONGO_DB = 'kafka_web_attack_data'
MONGO_COLLECTION = 'consumer_records'
CSV_FILE = 'db/csic_database.csv'

def run_producer():
    try:
        producer_service = KafkaProducerService(KAFKA_TOPIC,
            KAFKA_BROKERS,
            CSV_FILE,
            logger, 
            LIMIT
        )
        logger.info("Producer Service sucessfully created.")
        producer_service.run()
        logger.info("Producer Service running")
    except Exception as e:
        logger.error(f"Producer encountered an error: {e}")

async def run_consumer():
    try:
        consumer_service = KafkaConsumerService(
            KAFKA_TOPIC,
            KAFKA_BROKERS,
            MONGO_URI,
            MONGO_DB,
            MONGO_COLLECTION,
            logger
        )
        logger.info("Consumer Service sucessfully created.")
        await consumer_service.run()
        logger.info("Consumer Service running")
    except Exception as e:
        logger.error(f"Consumer encountered an error: {e}")
    
async def run_extractor():
    try:
        extractor_service = MongoSummaryService(logger=logger)
        connector_service = SQLConnectorService(logger=logger)
        connector_service.create_sql_table()
        logger.info("Extractor Service successfully created")
        await extractor_service.run(connector_service)
        logger.info("Extractor Service running")
    except Exception as e:
        logger.error(f"Extractor encountered an error: {e}")

@app.on_event("startup")
async def on_startup():
# async def main():
    os.system('cls')
    producer_thread = threading.Thread(target=run_producer, daemon=True)
    producer_thread.start()

    consumer_task = asyncio.create_task(run_consumer())
    extractor_task = asyncio.create_task(run_extractor())

    await asyncio.gather(extractor_task)
    await asyncio.gather(consumer_task)
    
    if producer_thread and producer_thread.is_alive():
        producer_thread.join()

# @app.on_event("shutdown")
# async def on_shutdown():
#     # # Cancel consumer task
#     if consumer_task:
#         consumer_task.cancel()
#         try:
#             await consumer_task
#         except asyncio.CancelledError:
#             logger.info("Consumer task cancelled")

#     # Cancel extractor task
#     if extractor_task:
#         extractor_task.cancel()  
#         try:
#             await extractor_task  
#         except asyncio.CancelledError:
#             logger.info("Extractor task cancelled")

# if __name__ == "__main__":
#     asyncio.run(main())