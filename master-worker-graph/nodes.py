# nodes.py
import random
import asyncio
from typing import Literal
from states import MasterState, WorkerState


# 워커 그래프에 분배할 task를 생성한다.
def prepare_tasks(state: MasterState) -> dict:
    tasks = [
        {"task_id": f"task_{i}", "type": "data_processing", "data": {"value": random.randint(1, 100)}}
        for i in range(1, 9)
    ]
    return {"tasks": tasks}


def aggregate_results(state: MasterState) -> dict:
    """워커로부터 수집된 결과를 집계합니다."""
    print("\n--- 📊 워커 결과 집계 중 ---")

    if not state.worker_results:
        print("❌ 수집된 결과가 없습니다.")
        return {"final_result": {"status": "failed", "message": "No results collected"}}

    # 결과 처리 및 집계
    total_value = sum(result.get("processed_value", 0) for result in state.worker_results)
    average_value = total_value / len(state.worker_results) if state.worker_results else 0

    final_result = {
        "status": "success",
        "total_tasks": len(state.worker_results),
        "total_value": total_value,
        "average_value": average_value,
        "processed_results": state.worker_results
    }

    print(f"✅ 결과 집계 완료: 평균값 = {average_value:.2f}")
    return {"final_result": final_result}


# --- 워커 그래프 노드 함수 ---

def initialize_worker(state: WorkerState) -> dict:
    """워커 초기화 및 작업 준비"""
    print(f"🔧 워커 초기화: 작업 ID {state.task_id}")
    return {"status": "processing"}


async def process_data(state: WorkerState) -> dict:
    """데이터 처리 작업 수행"""
    print(f"⚙️ 작업 처리 중: {state.task_id}")

    # 실제 작업을 시뮬레이션하기 위한 지연
    await asyncio.sleep(random.uniform(0.5, 2.0))

    # 입력 데이터 처리
    input_value = state.input_data.get("data", {}).get("value", 0)

    # 간단한 처리 로직 (예: 값을 2배로)
    processed_value = input_value * 2

    processed_data = {
        "original_value": input_value,
        "processed_value": processed_value,
        "task_id": state.task_id
    }

    print(f"✅ 작업 완료: {state.task_id} - 값 {input_value} → {processed_value}")
    return {"processed_data": processed_data, "status": "completed"}


def handle_error(state: WorkerState) -> dict:
    """오류 처리"""
    print(f"❌ 작업 실패: {state.task_id}")
    return {"status": "failed"}


# --- 라우터 함수 ---

def worker_router(state: WorkerState) -> Literal["success", "error"]:
    """워커 그래프의 라우팅 결정"""
    # 실제 환경에서는 여기서 오류 조건을 확인할 수 있습니다
    # 예제에서는 90% 확률로 성공하도록 설정
    if random.random() < 0.9:
        return "success"
    else:
        return "error"
