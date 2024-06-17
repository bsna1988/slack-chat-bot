import os
from typing import List

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DenseRetriever
from haystack.schema import Document

doc_dir = 'Apache Beam Documentation/'

# make sure these indices do not collide with existing ones, the indices will be wiped clean
# before data is inserted
doc_index = "docs"
label_index = "labels"

# Get the host where Elasticsearch is running, default to localhost
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

# Connect to Elasticsearch
document_store = ElasticsearchDocumentStore(
    host=host,
    username="",
    password="",
    index=doc_index,
    label_index=label_index,
    embedding_field="emb",
    embedding_dim=768,
    excluded_meta_data=["emb"],
    similarity="cosine",
)


def index_documents(docs: List[Document], retriever: DenseRetriever):
    document_store.delete_documents()
    document_store.write_documents(docs)
    document_store.update_embeddings(retriever)
