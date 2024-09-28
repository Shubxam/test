import transformers as ts
from transformers import pipeline
import duckdb as db
import pandas as pd
from tqdm.auto import tqdm
from transformers.pipelines.pt_utils import KeyDataset
# import concurrent.futures
import logging
import time


def articles_generators():
    for headline in headlines:
        yield headline

if __name__=="__main__":
    logger = logging.getLogger()
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    # fetch articles data
    with db.connect('./database/ticker_data.db') as conn:
        articles_df = conn.execute('select * from article_data;').df()

    # get headlines in a list
    headlines = articles_df.headline.drop_duplicates().to_list()
    classifier = pipeline("sentiment-analysis", model="./models/distilroberta-finetuned-financial-news-sentiment-analysis", framework='pt', device='mps')
    
    start_time_2 = time.time()
    results = []
    for res in classifier(articles_generators()):
        results.append(res)
    logger.debug(f'time taken to process generator: {time.time() - start_time_2} seconds.')