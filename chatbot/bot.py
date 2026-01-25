from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from sqlalchemy import create_engine
from llama_index.core.utilities.sql_wrapper import SQLDatabase
from dotenv import load_dotenv
from llama_index.core.indices.struct_store.sql_query import (
    SQLTableRetrieverQueryEngine,
)
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
)
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from utils import table_schema_objs
import os

def main():
    load_dotenv("../.env")
    os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY")
    llm = OpenAI(temperature=0.1, model="gpt-5.2")

    engine = create_engine("sqlite:///../euroleague.db")
    sql_database = SQLDatabase(engine, include_tables=["games", "players", "players_teams", "players_average_stats", "teams"])
   

    table_node_mapping = SQLTableNodeMapping(sql_database)
    obj_index = ObjectIndex.from_objects(
        table_schema_objs,
        table_node_mapping,
        VectorStoreIndex,
        embed_model=OpenAIEmbedding(model="text-embedding-3-large"),
    )
    query_engine = SQLTableRetrieverQueryEngine(
        sql_database, obj_index.as_retriever(similarity_top_k=3), llm=llm, verbose=False #True
    )
    
    print("Chatbot ready :) !")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        try:
            result = query_engine.query(user_input)
            print("Bot:", result)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()