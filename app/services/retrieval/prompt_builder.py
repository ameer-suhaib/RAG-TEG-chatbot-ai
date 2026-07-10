from app.services.retrieval.models import RetrievalResult

class PromptBuilder:

    def build(self, retrieval):

        system_prompt = """
You are the official AI assistant for TEG.

Rules:
- Use ONLY the supplied context.
- Never use outside knowledge.
- If information is unavailable, say so.
- Always answer in the detected language.
- Include citations.
"""

        context = "\n\n".join(
            [
                f"""
Title: {chunk.title}
URL: {chunk.url}

{chunk.content}
"""
                for chunk in retrieval.chunks
            ]
        )

        user_prompt = f"""
Context
-------
{context}

Question
--------
{retrieval.query}
"""

        return system_prompt, user_prompt