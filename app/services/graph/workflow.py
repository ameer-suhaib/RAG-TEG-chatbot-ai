from langgraph.graph import StateGraph, START, END

from .state import ChatState
from .nodes import GraphNodes
from .memory import memory


def build_graph():
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