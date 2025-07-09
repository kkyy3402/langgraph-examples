import asyncio
from workflow import master_app


async def main():
    final_state_dict = await master_app.ainvoke({})

    # 최종 결과 출력
    if "final_result" in final_state_dict and final_state_dict["final_result"]:
        final_result = final_state_dict["final_result"]
        print("\n=== 📊 최종 결과 ===")
        print(f"총 처리된 작업: {final_result.get('total_tasks')}")
        print(f"총 값: {final_result.get('total_value')}")
        print(f"평균 값: {final_result.get('average_value'):.2f}")
    else:
        print("\n❌ 최종 결과가 없습니다.")


if __name__ == "__main__":
    asyncio.run(main())
