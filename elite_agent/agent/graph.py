"""LangGraph agent graph construction."""

from langgraph.graph import END, START, StateGraph

from ..config.settings import settings
from .nodes import enrich_context_node, reasoning_node, should_continue, tool_node
from .state import AgentState


def build_agent_graph():
    """Build and compile the EliteAgent LangGraph graph.

    The graph follows the ReAct pattern:

        START → enrich_context → reasoning → (tools → reasoning)* → END

    Returns:
        A compiled LangGraph ``CompiledGraph`` instance configured with
        ``recursion_limit`` derived from ``settings.agent_max_iterations``.
    """
    builder = StateGraph(AgentState)

    # Register nodes
    builder.add_node("enrich_context", enrich_context_node)
    builder.add_node("reasoning", reasoning_node)
    builder.add_node("tools", tool_node)

    # Define edges
    builder.add_edge(START, "enrich_context")
    builder.add_edge("enrich_context", "reasoning")
    builder.add_conditional_edges(
        "reasoning",
        should_continue,
        {"tools": "tools", "end": END},
    )
    builder.add_edge("tools", "reasoning")

    return builder.compile()
