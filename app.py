import os

from dotenv import load_dotenv
from haystack.nodes import EmbeddingRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import document_store
import preprocessor

load_dotenv()
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']

app = App(token=SLACK_BOT_TOKEN)

retriever = EmbeddingRetriever(
    document_store=document_store.document_store,
    embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1")

doc_dir = 'Apache Beam Documentation/'
documents = preprocessor.preprocess(doc_dir)
document_store.index_documents(docs=documents, retriever=retriever)

reader = FARMReader(model_name_or_path="deepset/deberta-v3-large-squad2",
                    use_gpu=True)
pipe = ExtractiveQAPipeline(reader, retriever)


@app.event("app_mention")
def mention_handler(body, say):
    prediction = pipe.run(
        query=body['event']['text'],
        params={
            "Retriever": {"top_k": 5},
            "Reader": {"top_k": 3}
        }
    )
    say(prediction['answers'][0].answer)


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
