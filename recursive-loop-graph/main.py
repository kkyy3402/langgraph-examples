# main.py
import asyncio
import time
from workflow import recursive_loop_graph
from states import IterativeState


async def main():
    """
    재귀적 루프 그래프 예제를 실행하는 메인 함수입니다.
    """
    print("\n=== 🔄 재귀적 루프 그래프 예제 ===\n")
    print("이 예제는 목표 값에 도달할 때까지 같은 노드를 반복적으로 실행하는 방법을 보여줍니다.")
    print("각 반복에서 현재 값은 랜덤하게 증가하며, 목표 값에 도달하거나 최대 반복 횟수에 도달하면 종료됩니다.\n")

    # 초기 상태 설정
    initial_state = IterativeState(
        current_value=0,
        target_value=100,
        max_iterations=20,
        data={"task_name": "값 증가 작업", "started_at": time.time()}
    )

    print(f"🎯 목표: {initial_state.current_value}에서 시작하여 {initial_state.target_value} 이상 도달하기")
    print(f"⏱️ 제한: 최대 {initial_state.max_iterations}회 반복\n")

    # 시작 시간 기록
    start_time = time.time()

    # 재귀 루프 그래프 실행
    final_state = await recursive_loop_graph.ainvoke(initial_state)

    # 종료 시간 기록
    end_time = time.time()

    # 결과 출력
    print("\n=== 📊 최종 결과 ===")
    print(f"⏱️ 실행 시간: {end_time - start_time:.4f}초")

    if "data" in final_state and "final_value" in final_state["data"]:
        result_data = final_state["data"]
        print(f"📈 최종 값: {result_data['final_value']}")
        print(f"🔄 총 반복 횟수: {result_data['iterations']}")
        print(f"✅ 성공 여부: {'성공' if result_data['success'] else '실패'}")


if __name__ == "__main__":
    asyncio.run(main())
