from typing import Any, Dict
from sqlalchemy import text
import pandas as pd


from llama_index.core import SQLDatabase
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex
from llama_index.core.indices.struct_store import SQLTableSchema
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import Settings as LISettings
from llama_index.llms.openai import AzureOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from .config import settings
from .deps import get_engine
from .guardrails import validate_sql, whitelist_tables, enforce_limit

# Configure LlamaIndex with Azure OpenAI
LISettings.llm = AzureOpenAI(
    model=settings.llm_model,
    deployment=settings.azure_deployment,
    api_key=settings.azure_api_key,
    azure_endpoint=settings.azure_endpoint
)

LISettings.embed_model = OpenAIEmbedding(model=settings.embed_model)

engine = get_engine()
sqldb = SQLDatabase(engine)

node_mapping = SQLTableNodeMapping(sqldb)
schema_nodes = [SQLTableSchema(table_name=t) for t in sqldb.get_usable_table_names()]
obj_index = ObjectIndex.from_objects(objects=schema_nodes, node_mapping=node_mapping)

query_engine = NLSQLTableQueryEngine(sql_database=sqldb, synthesize_response=True)

def run_sql(sql: str) -> Dict[str, Any]:
    validate_sql(sql)
    whitelist_tables(sql)
    sql = enforce_limit(sql, settings.max_rows)
    with timed("sql_exec"):
        df = pd.read_sql(text(sql), engine)
    return {"sql": sql, "rows": df.to_dict(orient="records"), "rowcount": len(df)}

def ask_sql(question: str) -> Dict[str, Any]:
    with timed("nl2sql"):
        candidate = query_engine.query(question)
    sql = getattr(candidate, "metadata", {}).get("sql_query") or str(candidate)
    result = run_sql(sql)
    result.update({"question": question})
    return result