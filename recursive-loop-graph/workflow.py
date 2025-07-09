# workflow.py
from langgraph.constants import START
from langgraph.graph import StateGraph, END
from states import IterativeState
from nodes import process_step, finalize_result, completion_router


def create_recursive_loop_graph():
    """
    재귀적 루프 그래프를 생성합니다.
    이 그래프는 작업이 완료될 때까지 같은 노드를 반복적으로 실행합니다.
    """
    # 그래프 생성
    graph_builder = StateGraph(IterativeState)
    
    # 노드 추가
    graph_builder.add_node("process_step", process_step)
    graph_builder.add_node("finalize_result", finalize_result)
    
    # 시작 엣지
    graph_builder.add_edge(START, "process_step")
    
    # 조건부 엣지 추가 - 핵심 재귀 루프 구현
    graph_builder.add_conditional_edges(
        "process_step",  # 소스 노드
        completion_router,  # 라우터 함수
        {
            "continue": "process_step",  # 자기 자신으로 돌아가는 재귀 루프
            "complete": "finalize_result"  # 작업 완료 시 다음 단계로
        }
    )
    
    # 종료 엣지
    graph_builder.add_edge("finalize_result", END)
    
    # 그래프 컴파일
    return graph_builder.compile()


# 재귀 루프 그래프 인스턴스 생성
recursive_loop_graph = create_recursive_loop_graph()

# 다이어그램 생성
try:
    image_data = recursive_loop_graph.get_graph().draw_mermaid_png()
    with open("recursive_loop_diagram.png", "wb") as f:
        f.write(image_data)
    print("✅ 성공: 'recursive_loop_diagram.png' 파일이 생성되었습니다.")
except Exception as e:
    print(f"⚠️ 실패: 다이어그램 생성에 실패했습니다: {e}")
