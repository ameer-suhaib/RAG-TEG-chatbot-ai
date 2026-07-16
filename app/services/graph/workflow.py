"""Compile the RAG chat graph with in-memory thread checkpointing."""

from langgraph.graph import END, START, StateGraph

from .memory import memory
from .nodes import GraphNodes
from .state import ChatState


def build_graph():
    """Build: START → retrieve → prompt → llm → citation → END.

    The InMemorySaver checkpointer stores ``ChatState.messages`` per thread_id
    so follow-up questions keep conversation history.
    """
    nodes = GraphNodes()
    builder = StateGraph(ChatState)

    builder.add_node("retrieve", nodes.retrieval_node)
    builder.add_node("prompt", nodes.prompt_node)
    builder.add_node("llm", nodes.llm_node)
    builder.add_node("citation", nodes.citation_node)

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "prompt")
    builder.add_edge("prompt", "llm")
    builder.add_edge("llm", "citation")
    builder.add_edge("citation", END)

    return builder.compile(checkpointer=memory)
