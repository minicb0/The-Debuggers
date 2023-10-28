from haystack.nodes import FARMReader
from haystack.utils import fetch_archive_from_http
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from haystack.pipelines import ExtractiveQAPipeline
from haystack.utils import print_answers
import nltk
from pprint import pprint
import pickle
import logging
import os

nltk.download("all")

reader = FARMReader(model_name_or_path="distilbert-base-uncased-distilled-squad", use_gpu=True)

data_dir = "app/nlp_engine/data/base_data"

fetch_archive_from_http(
    url="https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-downstream/squad20.tar.gz", output_dir=data_dir
)

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

doc_dir = "app/nlp_engine/data/fine_tune_data"

fetch_archive_from_http(
    url="https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip",
    output_dir=doc_dir,
)

files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
document_store = InMemoryDocumentStore(use_bm25=True)
indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run_batch(file_paths=files_to_index)

retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
pipe = ExtractiveQAPipeline(reader, retriever)

prediction = pipe.run(
    query="Who is the father of Arya Stark?", params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
)

pprint(prediction)

print_answers(prediction, details="minimum")  ## Choose from `minimum`, `medium`, and `all`

file_path = "/content/drive/MyDrive/PMSM/roberta.pkl"

# Create a dictionary to hold the components of the pipeline
pipeline_components = {
    "retriever": retriever,
    "reader": reader
}

# Save the pipeline to a pickle file
with open(file_path, "wb") as file:
    pickle.dump(pipeline_components, file)