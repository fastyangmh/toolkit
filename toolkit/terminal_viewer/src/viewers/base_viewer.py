# import
from abc import ABC, abstractmethod
from typing import Any


# class
class BaseViewer(ABC):
    @abstractmethod
    def _load_data(self, source: Any) -> Any: ...

    @abstractmethod
    def _get_metadata(self, data: Any) -> dict[str, Any]: ...

    @abstractmethod
    def _display_data(
        self,
        source: Any,
        data: Any,
        metadata: dict[str, Any],
        **kwargs,
    ) -> None: ...

    def display(self, source: Any, **kwargs) -> None:
        data = self._load_data(source)
        metadata = self._get_metadata(data)

        self._display_data(source, data, metadata, **kwargs)
