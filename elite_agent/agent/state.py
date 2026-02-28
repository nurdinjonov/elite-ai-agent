"""LangGraph AgentState definition."""

from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """State object passed between graph nodes.

    Attributes:
        messages: Conversation history managed by LangGraph's *add_messages*
            reducer (automatically merges new messages).
        long_term_context: Relevant memories retrieved from the long-term store.
        knowledge_context: Relevant chunks retrieved from the RAG knowledge base.
    """

    messages: Annotated[list[BaseMessage], add_messages]
    long_term_context: str
    knowledge_context: str
