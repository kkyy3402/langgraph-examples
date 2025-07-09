# states.py
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class IterativeState(BaseModel):
    """
    반복적 작업을 처리하는 그래프의 상태를 정의합니다.
    
    Attributes:
        data: 처리할 데이터
        current_value: 현재 처리 중인 값
        target_value: 목표 값 (이 값에 도달하면 작업 완료)
        iterations: 현재까지의 반복 횟수
        max_iterations: 최대 허용 반복 횟수 (무한 루프 방지)
        is_complete: 작업 완료 여부
    """
    data: Dict[str, Any] = Field(default_factory=dict)
    current_value: int = 0
    target_value: int = 100
    iterations: int = 0
    max_iterations: int = 20  # 무한 루프 방지
    is_complete: bool = False
