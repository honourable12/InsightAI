from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class DatasetBase(BaseModel):
    name: str
    description: Optional[str] = None

class DatasetCreate(DatasetBase):
    pass

class DatasetResponse(DatasetBase):
    id: int
    user_id: int
    file_type: str
    columns: List[str]
    row_count: int
    created_at: datetime

    class Config:
        orm_mode = True

class AnalysisResponse(BaseModel):
    id: int
    dataset_id: int
    text_column: str
    created_at: datetime
    sentiment_counts: Dict[str, int]
    sample_results: List[Dict[str, Any]]

    class Config:
        orm_mode = True