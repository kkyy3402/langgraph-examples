# nodes.py
import random
from typing import Literal
from states import IterativeState


def process_step(state: IterativeState) -> dict:
    """
    반복적인 작업을 수행하는 노드입니다.
    작업이 완료될 때까지 자기 자신을 계속 호출합니다.
    """
    # 반복 횟수 증가
    iterations = state.iterations + 1

    # 현재 값 업데이트 (예: 랜덤하게 증가)
    current_value = state.current_value + random.randint(5, 15)

    print(f"🔄 반복 {iterations}: 현재 값 = {current_value} / 목표 값 = {state.target_value}")

    # 작업 완료 여부 확인
    is_complete = False
    if current_value >= state.target_value:
        is_complete = True
        print(f"✅ 목표 달성! 총 {iterations}번 반복 후 값 {current_value} 도달")
    elif iterations >= state.max_iterations:
        is_complete = True
        print(f"⚠️ 최대 반복 횟수({state.max_iterations}회) 도달. 작업 강제 종료.")

    return {
        "current_value": current_value,
        "iterations": iterations,
        "is_complete": is_complete
    }


def finalize_result(state: IterativeState) -> dict:
    """
    최종 결과를 정리하는 노드입니다.
    """
    success = state.current_value >= state.target_value

    if success:
        print(f"🎉 작업 성공! 목표 값 {state.target_value}에 도달했습니다.")
    else:
        print(f"❌ 작업 실패! 최대 반복 횟수에 도달했지만 목표 값에 도달하지 못했습니다.")
        print(f"   현재 값: {state.current_value}, 목표 값: {state.target_value}")

    return {
        "data": {
            **state.data,
            "final_value": state.current_value,
            "iterations": state.iterations,
            "success": success
        }
    }


def completion_router(state: IterativeState) -> Literal["continue", "complete"]:
    """
    작업 완료 여부에 따라 계속 반복할지 종료할지 결정하는 라우터 함수입니다.
    """
    if state.is_complete:
        return "complete"
    else:
        return "continue"
