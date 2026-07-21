# RAG-TEG-chatbot-ai

RAG application using LangChain and LangGraph.

## LangSmith tracing

1. Create an API key at [smith.langchain.com](https://smith.langchain.com).
2. Add to your `.env` (see `.env.example`):

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_...
LANGSMITH_PROJECT=teg-chatbot-ai
```

3. Restart the API. Chat and stream runs appear under that project in LangSmith.
