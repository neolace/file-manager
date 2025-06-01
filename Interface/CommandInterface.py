class CommandInterface(ABC):
    """Base interface for all commands"""

    @abstractmethod
    def validate(self, args: Namespace) -> None:
        pass

    @abstractmethod
    def execute(self, args: Namespace, logger: logging.Logger) -> None:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass
