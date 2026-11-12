from typing import TypedDict, Annotated,Any
from langgraph.graph.message import add_messages


class GraphState(TypedDict):
    messages=Annotated[list,add_messages]

    table1Path:str
    table2Path:str
    profile:dict[str,Any]
    candidatesFromSchemaMatching:list[dict]
    finalMatches:list[dict]
    