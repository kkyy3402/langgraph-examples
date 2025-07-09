# workflow.py
from functools import partial
import asyncio

from langgraph.constants import START
from langgraph.graph import StateGraph, END
from states import MasterState, WorkerState
from nodes import (
    prepare_tasks,
    aggregate_results,
    initialize_worker,
    process_data,
    handle_error,
    worker_router
)


# --- 워커 그래프 생성 함수 ---
def create_worker_graph(worker_id: str):
    """워커 그래프를 생성합니다."""
    graph_builder = StateGraph(WorkerState)

    # 노드 추가
    graph_builder.add_node("initialize", initialize_worker)
    graph_builder.add_node("process", process_data)
    graph_builder.add_node("handle_error", handle_error)

    # 엣지 연결
    graph_builder.add_edge(START, "initialize")
    graph_builder.add_edge("initialize", "process")

    # 조건부 엣지 추가
    graph_builder.add_conditional_edges(
        "process",
        worker_router,
        {
            "success": END,
            "error": "handle_error"
        }
    )

    graph_builder.add_edge("handle_error", END)

    # 그래프 컴파일
    worker_graph = graph_builder.compile()

    # 다이어그램 생성 (선택 사항)
    try:
        image_data = worker_graph.get_graph().draw_mermaid_png()
        with open(f"worker_{worker_id}_diagram.png", "wb") as f:
            f.write(image_data)
        print(f"✅ 성공: 'worker_{worker_id}_diagram.png' 파일이 생성되었습니다.")
    except Exception as e:
        print(f"⚠️ 실패: 워커 다이어그램 생성에 실패했습니다: {e}")

    return worker_graph


# --- 워커 그래프 인스턴스 생성 ---
worker_graph_1 = create_worker_graph("1")
worker_graph_2 = create_worker_graph("2")


# --- 워커 실행 함수 ---
async def run_worker(worker_graph, task):
    """워커 그래프를 실행합니다."""
    initial_state = WorkerState(
        task_id=task["task_id"],
        input_data=task
    )

    try:
        # worker_graph.ainvoke는 딕셔너리를 반환하므로 상태 객체가 아닙니다
        final_state_dict = await worker_graph.ainvoke(initial_state)

        # 상태 딕셔너리에서 필요한 정보 추출
        status = final_state_dict.get("status", "failed")
        processed_data = final_state_dict.get("processed_data")

        if status == "completed" and processed_data:
            return processed_data
        else:
            return {"task_id": task["task_id"], "status": "failed", "processed_value": 0}
    except Exception as e:
        print(f"❌ 워커 실행 중 오류 발생: {e}")
        return {"task_id": task["task_id"], "status": "failed", "processed_value": 0}


# --- 마스터 그래프 노드 함수 (워커 호출) ---
async def execute_workers(state: MasterState) -> dict:
    tasks = state.tasks
    if not tasks:
        return {"worker_results": []}

    # 태스크를 두 워커 그래프에 분배
    worker1_tasks = tasks[::2]  # task중 짝수는 worker1에 할당
    worker2_tasks = tasks[1::2]  # task중 호루는 worker2에 할당

    print(f"📦 워커 1에 {len(worker1_tasks)}개 작업 할당")
    print(f"📦 워커 2에 {len(worker2_tasks)}개 작업 할당")

    worker1_task = asyncio.gather(
        *[run_worker(worker_graph_1, task) for task in worker1_tasks]
    )

    worker2_task = asyncio.gather(
        *[run_worker(worker_graph_2, task) for task in worker2_tasks]
    )

    # 두 워커 병렬 실행
    worker1_results, worker2_results = await asyncio.gather(worker1_task, worker2_task)

    # 결과 합치기
    all_results = worker1_results + worker2_results

    print(f"✅ 모든 워커 작업 완료: {len(all_results)}개 결과 수집")
    return {"worker_results": all_results}


# --- 마스터 그래프 생성 ---
master_graph_builder = StateGraph(MasterState)

# 노드 추가
master_graph_builder.add_node("prepare_tasks", prepare_tasks)
master_graph_builder.add_node("execute_workers", execute_workers)
master_graph_builder.add_node("aggregate_results", aggregate_results)

# 엣지 연결
master_graph_builder.add_edge(START, "prepare_tasks")
master_graph_builder.add_edge("prepare_tasks", "execute_workers")
master_graph_builder.add_edge("execute_workers", "aggregate_results")
master_graph_builder.add_edge("aggregate_results", END)

# 마스터 그래프 컴파일
master_app = master_graph_builder.compile()

# 다이어그램 생성
try:
    image_data = master_app.get_graph().draw_mermaid_png()
    with open("master_diagram.png", "wb") as f:
        f.write(image_data)
    print("✅ 성공: 'master_diagram.png' 파일이 생성되었습니다.")
except Exception as e:
    print(f"⚠️ 실패: 마스터 다이어그램 생성에 실패했습니다: {e}")
