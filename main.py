import asyncio
import threading
import logging
from fastapi import FastAPI
from consumer import KafkaConsumerService
from extractor import MongoSummaryService
from producer import KafkaProducerService

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
KAFKA_BROKERS = ['localhost:9092']
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'kafka_web_attack_data'
MONGO_COLLECTION = 'consumer_records'
CSV_FILE = 'csic_database.csv'

# # TODO:
LIMIT = None

def run_producer():
    try:
        producer_service = KafkaProducerService(logger=logger, limit=LIMIT)
        producer_service.create_producer(file=CSV_FILE)
        producer_service.send_message()
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
        await consumer_service.run()
    except Exception as e:
        logger.error(f"Consumer encountered an error: {e}")
    
async def run_extractor():
    logger.info("EXTRACTOR: Inside of run_extractor()")
    try:
        logger.info("EXTRACTOR: Attempting to create MongoSummaryService Object")
        extractor_service = MongoSummaryService(logger=logger)
        logger.info("EXTRACTOR: MongoSummaryService Object creating sucess...starting to run!")
        await extractor_service.run()
    except Exception as e:
        logger.error(f"Extractor encountered an error: {e}")


@app.on_event("startup")
async def on_startup():
    global producer_thread, consumer_task, extractor_task
    logger.info(f"Starting producer, consumer and extractor")

    # # Start producer task
    producer_thread = threading.Thread(target=run_producer, daemon=True)
    producer_thread.start()
    logger.info(f"Producer started")
  

    # consumer_task = asyncio.create_task(run_consumer())
    # logger.info(f"Consumer started")
    await run_consumer()

    logger.info(f"Extractor started")
    # extractor_task = asyncio.create_task(run_extractor())
    await run_extractor()
    # await asyncio.gather(producer_thread, consumer_task, extractor_task)
    logger.info(f"Producer, consumer and extractor started")


@app.on_event("shutdown")
async def on_shutdown():
    global producer_thread, consumer_task, extractor_task
    logger.info(f"Shutting down producer, consumer and extractor")

    # # Stop producer thread
    if producer_thread and producer_thread.is_alive():
        producer_thread.join()

    # # Cancel consumer task
    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            logger.info("Consumer task cancelled")

    # Cancel extractor task
    if extractor_task:
        extractor_task.cancel()  
        try:
            await extractor_task  
        except asyncio.CancelledError:
            logger.info("Extractor task cancelled")

    logger.info(f"Producer, consumer and extractor shutdown complete")

# SANITY CHECK! 
@app.get("/")
async def health_check():
    return {"message": "Application is running!"}