
from src.graph.workflow import buildGraph
from src.sparkSession import getSparkSession

def main():
    app=buildGraph()
    initialState={
        "messages":[],
        "table1Path":"PATH IN HDFS",
        "table2Path":"PATH IN HDFS",
        "profiles":{},
        "candidatesFromSchemaMatching":[],
        "finalMatches":[]

    }

for step in app.stream(initialState,stream_mode="values"):
    latestMessage=step["messages"][-1] if step["messages"] else None
    if latestMessage:
        if hasattr(latestMessage,"tool_calls") and latestMessage.tool_calls:
            for toolCall in latestMessage.tool_calls:
                print("f[Agent's Choice] Tool: {toolCall['name'] with Args:{toolCall['args']}}")
        elif latestMessage.type=='ai' and  latestMessage.content:
            print("\n Final Join Decision: "):
            print(latestMessage.content)

getSparkSession().stop()

