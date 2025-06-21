# import
from abc import ABC, abstractmethod
from typing import Any, Sequence


# class
class BaseModel(ABC):
    @abstractmethod
    def transcribe(self, inputs: Sequence[Any], *args, **kwargs) -> Any: ...
