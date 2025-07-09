# state.py
from typing import TypedDict, Optional, NotRequired

from pydantic import BaseModel


class TrainingState(BaseModel):
    iterations: int = 0
    model: Optional[str] = None
    evaluation: Optional[str] = None
    loss: Optional[float] = 1.0
