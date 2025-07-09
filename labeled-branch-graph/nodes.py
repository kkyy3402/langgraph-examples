# nodes.py
from state import TrainingState


# (다른 노드 함수들은 변경 없음)
def retrieve_data(state: TrainingState) -> dict:
    return {"iterations": 0}


def train_model(state: TrainingState) -> dict:
    return {"model": "trained_model"}


def evaluate_model(state: TrainingState) -> dict:
    evaluation = "insufficient"
    return {"evaluation": evaluation}


def adjust_parameters(state: TrainingState) -> dict:
    current_iterations = state.iterations
    next_loss = state.loss - 0.1
    return {"iterations": current_iterations + 1, "loss": next_loss}


def visualize_performance(state: TrainingState) -> dict:
    print("📈 성과 시각화")
    return {}


def handle_stop_condition(state: TrainingState) -> dict:
    print("🛑 중단 처리")
    return {}


def evaluation_router(state: TrainingState) -> str:
    if state.loss < 0.5:
        return "stop"

    if state.iterations >= 10:
        print("🔔 최대 반복 횟수 (10회)에 도달하여 워크플로우를 종료합니다.")
        return "force_stop"  # 새로운 종료 조건 키 반환

    return state.evaluation
