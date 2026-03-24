import streamlit as st
# Using StreamlitCallbackHandler to display thoughts and actions of an agent
from langchain.callbacks import StreamlitCallbackHandler
from agent import create_agent

st.title("Agentic Search with LangChain 🦜 using arXiv, Wikipedia & DuckDuckGo")

## Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Groq API Key:",type="password")

#Session state
if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assisstant","content":"Hi,I'm a chatbot who can search the web. How can I help you?"}
    ]

#Show messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

if prompt:=st.chat_input(placeholder="What is Generative AI?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    if not api_key:
        st.warning("Please enter your API key.")
        st.stop()
    search_agent = create_agent(api_key)

    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({'role':'assistant',"content":response})
        st.write(response)

