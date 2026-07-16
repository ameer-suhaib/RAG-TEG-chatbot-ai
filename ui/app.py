import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8002/app/v1"


st.set_page_config(
    page_title="TEG AI Assistence",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 TEG AI Assistence")

st.caption("Poweres by RAG + LangGraph")

### Side bar ####

st.sidebar.title("Knowladge Base")


if "thread_id" not in st.session_state:

    st.session_state.thread_id = str(
        uuid.uuid4()
    )

st.sidebar.caption(f"thread_id: `{st.session_state.thread_id}`")

if st.sidebar.button("New chat"):
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.rerun()

if st.sidebar.button("Start Ingestion"):
    with st.spinner("Building knowladge base..."):
        response = requests.post(f"{API_URL}/start")

        if response.status_code == 200:
            st.sidebar.success("Knowladge base updated")
            st.sidebar.json(response.json())
        else:
            st.sidebar.error(response.text)


# ------------------------
# Chat
# ------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about TEG..")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        answer = ""

        try:
            with requests.post(
                f"{API_URL}/chat",
                json={
                    "question": prompt,
                    "thread_id": st.session_state.thread_id,
                },
                stream=True,
                timeout=120,
            ) as response:
                if not response.ok:
                    placeholder.error(response.text)
                else:
                    for chunk in response.iter_content(
                        chunk_size=None,
                        decode_unicode=True,
                    ):
                        if chunk:
                            answer += chunk
                            placeholder.markdown(answer + "▌")

                    placeholder.markdown(answer)

                    if answer:
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": answer,
                            }
                        )
        except requests.RequestException as exc:
            placeholder.error(f"Request failed: {exc}")
