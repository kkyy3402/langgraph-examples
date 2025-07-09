# workflow.py
from langgraph.constants import START
from langgraph.graph import StateGraph, END
from state import TrainingState
from nodes import (
    retrieve_data,
    train_model,
    evaluate_model,
    adjust_parameters,
    visualize_performance,
    handle_stop_condition,
    evaluation_router,
)

# 1. 그래프 생성
graph_builder = StateGraph(TrainingState)

# 2. 노드 추가 (변경 없음)
graph_builder.add_node("retrieve_data", retrieve_data)
graph_builder.add_node("train_model", train_model)
graph_builder.add_node("evaluate_model", evaluate_model)
graph_builder.add_node("adjust_parameters", adjust_parameters)
graph_builder.add_node("visualize_performance", visualize_performance)
graph_builder.add_node("handle_stop_condition", handle_stop_condition)

# 3. 엣지 연결
graph_builder.add_edge(START, "retrieve_data")
graph_builder.add_edge("retrieve_data", "train_model")
graph_builder.add_edge("train_model", "evaluate_model")

graph_builder.add_conditional_edges(
    "evaluate_model",
    evaluation_router,
    {
        "insufficient": "adjust_parameters",
        "sufficient": "visualize_performance",
        "stop": "handle_stop_condition",
        "force_stop": END,
    }
)

# 6. 루프 및 종료 설정 (변경 없음)
graph_builder.add_edge("adjust_parameters", "train_model")
graph_builder.add_edge("visualize_performance", END)
graph_builder.add_edge("handle_stop_condition", END)

# 7. 그래프 컴파일
app = graph_builder.compile()

# --- 변경 사항: 그래프 다이어그램을 PNG 파일로 저장 ---
print("⏳ 워크플로우 다이어그램 생성 시도...")
try:
    # get_graph()로 그래프 객체를 얻고, draw_png()로 이미지 데이터 생성
    image_data = app.get_graph().draw_mermaid_png()
    with open("diagram.png", "wb") as f:
        f.write(image_data)
    print("✅ 성공: 'diagram.png' 파일이 생성되었습니다.")
except Exception as e:
    print(f"⚠️ 실패: 다이어그램 생성에 필요한 라이브러리가 설치되지 않았을 수 있습니다. (graphviz, pydot)")
    print(f"   macOS: 'brew install graphviz' / Ubuntu: 'sudo apt-get install graphviz'")
    print(f"   Python: 'pip install pydot pygraphviz'")
    print(f"   오류: {e}")
