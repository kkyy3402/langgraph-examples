# nodes.py
import httpx
from states import ParallelRequestState

API_URL = "http://localhost:8080/echo"


# payload 준비
def prepare_requests(state: ParallelRequestState) -> dict:
    payloads = [
        {"request_id": i, "message": f"Hello from agent {i}"}
        for i in range(1, 5)
    ]
    return {"request_payloads": payloads}


# 이 함수는 단순히, API 호출을 하는 역할만 수행한다.
async def fetch_single_data(state: ParallelRequestState, index: int) -> dict:
    payload = state.request_payloads[index]
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, json=payload)
            result = response.json()
            print(f"✅ 에이전트 {index + 1}가 응답 수신: {result}")
            return {"fetch_results": [result]}

        except httpx.TimeoutException:
            return {"fetch_results": []}

        except httpx.ConnectError as e:
            return {"fetch_results": []}


def process_results(state: ParallelRequestState) -> dict:
    """모든 병렬 작업의 결과를 취합하여 출력하는 노드."""
    print("\n--- 📊 최종 수집 결과 (순서는 보장되지 않음) ---")
    if not state.fetch_results:
        print("데이터를 가져오지 못했습니다.")
    else:
        # ID를 기준으로 정렬하여 출력
        sorted_results = sorted(state.fetch_results, key=lambda r: r.get('request_id', 0))
        for result in sorted_results:
            print(f"  - 수신 데이터: {result}")

    return {}
