# workflow.py
from functools import partial

from langgraph.constants import START
from langgraph.graph import StateGraph, END
from states import ParallelRequestState
from nodes import prepare_requests, fetch_single_data, process_results


def create_agent_node(index: int):
    async def agent_node(state: ParallelRequestState):
        return await fetch_single_data(state, index=index)

    return agent_node


graph_builder = StateGraph(ParallelRequestState)

graph_builder.add_node("prepare_requests", prepare_requests)
graph_builder.add_node("process_results", process_results)

agent_count = 4
for i in range(agent_count):
    node_name = f"fetch_agent_{i + 1}"
    agent_function = create_agent_node(index=i)
    graph_builder.add_node(node_name, agent_function)

# START -> Prepare Request
graph_builder.add_edge(START, "prepare_requests")

# Fan-in
for i in range(agent_count):
    graph_builder.add_edge("prepare_requests", f"fetch_agent_{i + 1}")

# Fan-out. 자바스크립트의 Promise.all 처럼 동작
for i in range(agent_count):
    graph_builder.add_edge(f"fetch_agent_{i + 1}", "process_results")

graph_builder.add_edge("process_results", END)

app = graph_builder.compile()

# 다이어그램 그리기.
try:
    image_data = app.get_graph().draw_mermaid_png()
    with open("diagram.png", "wb") as f:
        f.write(image_data)
    print("✅ 성공: 'diagram.png' 파일이 생성되었습니다.")
except Exception as e:
    print(f"⚠️ 실패: Mermaid 다이어그램 생성에 실패했습니다: {e}")
