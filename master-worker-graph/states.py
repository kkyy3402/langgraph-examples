# states.py
import operator
from typing import List, Dict, Any, Optional, Annotated
from pydantic import BaseModel, Field


class WorkerState(BaseModel):
    task_id: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
    processed_data: Optional[Dict[str, Any]] = None
    status: str = "pending"


class MasterState(BaseModel):
    tasks: List[Dict[str, Any]] = Field(default_factory=list)

    # Fan-in을 위한 Annotated 타입 사용
    worker_results: Annotated[List[Dict[str, Any]], operator.add] = Field(default_factory=list)
    final_result: Optional[Dict[str, Any]] = None
