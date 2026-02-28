"""LangGraph node functions for EliteAgent."""

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode

from ..config.settings import settings
from ..knowledge.ingest import KnowledgeBase
from ..memory.long_term import LongTermMemory
from ..tools import ALL_TOOLS
from .prompts import SYSTEM_PROMPT
from .state import AgentState

# Shared LLM instances
llm = ChatOpenAI(
    model=settings.openai_model,
    temperature=0.1,
    api_key=settings.openai_api_key,
)
llm_with_tools = llm.bind_tools(ALL_TOOLS)

# Shared memory / knowledge instances (lazy; initialised on first call)
_long_term_memory: LongTermMemory | None = None
_knowledge_base: KnowledgeBase | None = None


def _get_long_term_memory() -> LongTermMemory:
    global _long_term_memory  # noqa: PLW0603
    if _long_term_memory is None:
        _long_term_memory = LongTermMemory()
    return _long_term_memory


def _get_knowledge_base() -> KnowledgeBase:
    global _knowledge_base  # noqa: PLW0603
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------


def enrich_context_node(state: AgentState) -> dict:
    """Retrieve relevant context from long-term memory and the knowledge base.

    Extracts the latest user message and uses it as a query to populate
    ``long_term_context`` and ``knowledge_context`` in the state.

    Args:
        state: Current agent state.

    Returns:
        A partial state dict with updated context fields.
    """
    messages = state.get("messages", [])
    query = ""
    for msg in reversed(messages):
        if hasattr(msg, "type") and msg.type == "human":
            query = msg.content if isinstance(msg.content, str) else str(msg.content)
            break

    long_term_context = ""
    knowledge_context = ""

    if query:
        try:
            ltm = _get_long_term_memory()
            long_term_context = ltm.recall_as_text(query, k=5)
        except Exception:  # noqa: BLE001
            long_term_context = ""

        try:
            kb = _get_knowledge_base()
            kb_results = kb.query(query, k=5)
            if kb_results:
                lines = [
                    f"{i}. {r['content'][:300]} (manba: {r['source']}, score: {r['score']})"
                    for i, r in enumerate(kb_results, start=1)
                ]
                knowledge_context = "\n".join(lines)
        except Exception:  # noqa: BLE001
            knowledge_context = ""

    return {
        "long_term_context": long_term_context,
        "knowledge_context": knowledge_context,
    }


def reasoning_node(state: AgentState) -> dict:
    """Send the conversation history (with system prompt) to the LLM.

    Args:
        state: Current agent state.

    Returns:
        A partial state dict containing the new AI message.
    """
    system_content = SYSTEM_PROMPT.format(
        agent_name=settings.agent_name,
        long_term_context=state.get("long_term_context") or "Mavjud emas.",
        knowledge_context=state.get("knowledge_context") or "Mavjud emas.",
    )
    system_message = SystemMessage(content=system_content)
    messages = [system_message] + list(state.get("messages", []))
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    """Routing function — decides whether to call tools or end the turn.

    Args:
        state: Current agent state.

    Returns:
        ``"tools"`` if the last message contains tool calls, otherwise
        ``"end"``.
    """
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return "end"


# Pre-built tool execution node
tool_node = ToolNode(ALL_TOOLS)
