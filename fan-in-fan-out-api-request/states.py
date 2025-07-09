# state.py
import operator
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Annotated


class ParallelRequestState(BaseModel):
    """
    Fan-out/Fan-in 워크플로우의 상태를 정의합니다.

    Attributes:
        request_payloads: API에 보낼 요청 데이터 목록
        fetch_results: 병렬 노드로부터 수집된 결과 목록.
                       Annotated를 사용하여 결과가 누적되도록 합니다.
    """
    request_payloads: List[Dict[str, Any]] = Field(default_factory=list)

    # --- ★★★ Fan-in의 핵심 ★★★ ---
    # fetch_results 필드에 새로운 값이 들어올 때마다,
    # 기존 값에 더해지도록(operator.add) LangGraph에 지시합니다.
    # 예: [1] + [2] -> [1, 2]
    fetch_results: Annotated[List[Dict[str, Any]], operator.add] = []
