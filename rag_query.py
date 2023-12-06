from llama_index import StorageContext,load_indices_from_storage, load_index_from_storage
from llama_index.graph_stores import NebulaGraphStore
import os
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config
from llama_index.prompts import PromptTemplate
from llama_index.llms import HuggingFaceLLM
from langchain.embeddings import HuggingFaceEmbeddings
from llama_index import (
    KnowledgeGraphIndex,
    ServiceContext,
    SimpleDirectoryReader,
)

os.environ["GRAPHD_HOST"] = "127.0.0.1"
os.environ["NEBULA_USER"] = "root"
os.environ["NEBULA_PASSWORD"] = "nebula"
os.environ["NEBULA_ADDRESS"] = "127.0.0.1:9669"

config = Config()
config.max_connection_pool_size = 10
connection_pool = ConnectionPool()
connection_pool.init([('127.0.0.1', 9669)], config)

session = connection_pool.get_session('root', 'nebula')

space_name = "phillies_rag"
edge_types, rel_prop_names = ["relationship"], ["relationship"]
tags = ["entity"]

graph_store = NebulaGraphStore(
    space_name=space_name,
    edge_types=edge_types,
    rel_prop_names=rel_prop_names,
    tags=tags,
)
storage_context = StorageContext.from_defaults(persist_dir='./storage_graph', graph_store=graph_store)

query_wrapper_prompt = PromptTemplate("사용자가 한 말을 읽고 그에 질문에 답하거나 명령에 응답하는 비서입니다.\n\n{query_str}\n\n비서:")

llm = HuggingFaceLLM(
    context_window=2048,
    max_new_tokens=100,
    generate_kwargs={"temperature":0.25, "do_sample": True},
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name="Minirecord/Mini_DPO_7b_01",
    model_name="Minirecord/Mini_DPO_7b_01",
    device_map="auto",
)
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
service_context = ServiceContext.from_defaults(chunk_size=512, llm=llm, embed_model=embed_model)

kg_index = load_index_from_storage(
    storage_context=storage_context,
    service_context=service_context,
    max_triplets_per_chunk=15,
    space_name=space_name,
    edge_types=edge_types,
    rel_prop_names=rel_prop_names,
    tags=tags,
)
query_engine = kg_index.as_query_engine(streaming=True)
response = query_engine.query("수원 삼성에 대한 사실들을 나열해줘.")
response.print_response_stream()
session.release()