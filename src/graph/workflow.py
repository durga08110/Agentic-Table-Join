from langchain_core.messages improt HumanMessage,SystemMessage
from langchain_openai import ChatOpenAI #change to other AI
from langgraph.graph import END,START,StateGraph
from langgraph.prebuilt import ToolNode,tools_condition

from src.graph.state import GraphState
from src.tools.embeddings import generateEmbeddings
from src.tools.matching import cosineSimilarity
from src.tools.matching import stringMatch
from src.tools.matching import editDistance
from src.tools.profiling import dataProfiling

#put all list of tools in a list
tools=[dataProfiling,
generateEmbeddings,
cosineSimilarity,
stringMatch,
editDistance]


llm=ChatOpenAI(model="gpt-4o",temperature=0).bind_tools(tools)
SYSTEM_PROMPT=""" """


def agentNode(state:GraphState):
    messages=state["messages"]
    if not messages:
        messages=[
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=f"Find join columns between Table 1 {state['table1Path']\nTable 2:{state['table2Path']}}"
            )
        ]
    response=llm.invoke(messages)
    return {"messages":[response]}


def buildGraph():
    workflow=StateGraph(GraphState)
    workflow.addNode("agent",agentNode)
    workflow.addNode("tools",ToolNode(tools))

    workflow.add_edge(START,"agent")
    workflow.add_conditional_edges("agent",tools_condition)

    workflow.add_edge("tools","agent")
    return workflow.compile()

    





