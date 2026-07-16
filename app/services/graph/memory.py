"""Shared checkpointer for per-thread chat memory (process-local)."""

from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()
