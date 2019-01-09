from abc import ABC, abstractmethod


class AbstractSource(ABC):
    """Abstract Source class that is used as the source"""

    @abstractmethod
    def set_source(self):
        pass
