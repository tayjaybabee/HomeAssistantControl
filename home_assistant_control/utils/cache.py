from abc import ABC, abstractmethod

from home_assistant_control.log_engine import Loggable
from home_assistant_control.utils import LOGGER as PARENT_LOGGER


LOGGER = PARENT_LOGGER.get_child('cache')


class Publisher(Loggable):
    """An interface for objects that can notify subscribers of events."""

    def __init__(self, parent_log_device=LOGGER):
        super().__init__(parent_log_device=parent_log_device)
        self.__subscribers = []

    def subscribe(self, subscriber):
        """Subscribe to events."""
        log = self.log_device.get_child('subscribe')
        log.logger.debug(f'Subscribing to {subscriber}')

        self.__subscribers.append(subscriber)

        log.logger.debug(f'Number of subscriptions: {len(self.__subscribers)}')

    def unsubscribe(self, subscriber):
        """Unsubscribe from events."""
        log = self.log_device.get_child('unsubscribe')
        log.logger.debug(f'Unsubscribing to {subscriber}')

        self.__subscribers.remove(subscriber)

        log.logger.debug(f'Number of subscriptions: {len(self.__subscribers)}')

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
