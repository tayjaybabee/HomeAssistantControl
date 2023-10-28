from abc import ABC, abstractmethod


class Publisher:
    """An interface for objects that can notify subscribers of events."""

    def __init__(self):
        self.__subscribers = []

    def subscribe(self, subscriber):
        """Subscribe to events."""
        self.__subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        """Unsubscribe from events."""
        self.__subscribers.remove(subscriber)

    def _notify(self):
        """Notify all subscribers."""
        for subscriber in self.__subscribers:
            subscriber.update()


class Subscriber(ABC):
    """An interface for objects that can receive notifications from publishers."""

    @abstractmethod
    def update(self):
        """Receive notification."""
        pass
