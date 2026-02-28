"""Short-term in-memory chat history."""

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import BaseMessage


class ShortTermMemory:
    """Manages short-term conversational memory using an in-memory store.

    Automatically trims old messages when the history exceeds *max_messages*.
    """

    def __init__(self, max_messages: int = 50) -> None:
        """Initialise the short-term memory store.

        Args:
            max_messages: Maximum number of messages to retain before trimming.
        """
        self._history = ChatMessageHistory()
        self.max_messages = max_messages

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_user_message(self, content: str) -> None:
        """Append a user message to the history.

        Args:
            content: The user's message text.
        """
        self._history.add_user_message(content)
        self._trim()

    def add_ai_message(self, content: str) -> None:
        """Append an AI message to the history.

        Args:
            content: The AI's response text.
        """
        self._history.add_ai_message(content)
        self._trim()

    def get_messages(self) -> list[BaseMessage]:
        """Return all stored messages.

        Returns:
            A list of :class:`~langchain_core.messages.BaseMessage` objects.
        """
        return self._history.messages

    def clear(self) -> None:
        """Remove all messages from the history."""
        self._history.clear()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _trim(self) -> None:
        """Remove the oldest messages when history exceeds *max_messages*."""
        messages = self._history.messages
        if len(messages) > self.max_messages:
            excess = len(messages) - self.max_messages
            self._history.messages = messages[excess:]
