# services/base_service.py
from abc import ABC, abstractmethod

class AbstractTaskService(ABC):
    """Abstract Base Class for all task services to ensure a consistent interface."""

    @abstractmethod
    def execute(self, *args, **kwargs) -> any:
        """The main execution method for the service."""
        pass
