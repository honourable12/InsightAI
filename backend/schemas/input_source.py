from enum import Enum
import sqlalchemy
from sqlalchemy.types import Enum as SQLAEnum

class InputSourceType(Enum):
    CSV = "csv"
    JSON = "json"
    API = "api"

# SQLAlchemy Enum Type for database compatibility
SQLAInputSourceType = SQLAEnum(InputSourceType)