from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


class PromptBuilder:

    def build(
        self,
        question: str,
        chunks: list[dict],
    ):
        system_prompt = """
You are the official AI assistant for TEG (Teastas Eorpach na Gaeilge).

Rules:
- Conversation history is part of the chat. Always use it for follow-ups and for facts the user told you (name, preferences, prior questions).
- For TEG website questions, answer using the supplied Context.
- Never invent TEG facts that are not in Context.
- If the user asks about something they already said in this conversation (e.g. "what is my name?"), answer from conversation history even if Context is empty or irrelevant.
- If you cannot answer from history or Context, say so.
- Answer in the same language as the user.
- When using Context, include citations.
"""

        context = "\n\n".join(
            [
                f"""
Title: {chunk['title']}
URL: {chunk['url']}

{chunk['content']}
"""
                for chunk in chunks
            ]
        ) if chunks else "(no website context retrieved)"

        user_prompt = f"""
Context
-------
{context}

Question
--------
{question}
"""

        return system_prompt, user_prompt
