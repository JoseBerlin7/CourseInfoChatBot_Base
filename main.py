import streamlit as st
from streamlit_chat import message as st_msg
# from streamlit_webrtc import webrtc_streamer
import random
import requests

from DM import DM

class main:
    def __init__(self):
        self.dm = DM()
        self.data = []
        self.UI()

        if "data" not in st.session_state:
            st.session_state.data = dict()
            st.session_state.site = ""
            st.session_state.sys_no = 2

    def load_data(self):
        st.session_state.data = self.dm.scraped_data  # to store the scraped & processed passages
        st.session_state.site = self.dm.source_site  # to store the source of the passages

    def Sys_switch(self):
        st.session_state.sys_no = self.dm.system_no  # to store which system we are currently working on

    def got_msg(self):
        input_text = st.session_state.input_text
        st.session_state.history.append({"message": input_text, "is_user": True})  # Updating the session state

        response, intent = self.dm.managing_convo(inp=input_text, data=st.session_state.data,
                                                  source=st.session_state.site, System_no=st.session_state.sys_no) # passing the input to DM

        if intent == "select course":
            self.load_data()            # storing the memory in cache
        elif intent == "switch system":
            self.Sys_switch()           # switching between different systems

        st.session_state.history.append({"message": response, "is_user": False})  # Updating the session state with the response recieved
        st.session_state.update(input_text="")

    def UI(self):
        consent_form = "https://forms.office.com/e/xK9xeHbSci"
        # Setting up the user interface
        st.title("Info Delivery Chatbot")

        # Creating a session if it doesn't already exists
        if "history" not in st.session_state:
            st.session_state.history = []

        st.write(
            "Welcome! I'm your Cbot.\n Today, I will be helping you with finding information about the courses available at Heriot Watt University.")
        st.write(
            f"\nBefore we start can you please fill the consent form:\n\t{consent_form}")
        st.write("\nTo end the conversation and move further to evaluation, use '\end' command")
        st.write("\nTo get started with, what course would you like to talk about today?")

        # Displaying the chat history
        # Create a container to hold chat history and text input
        chat_history = st.container()

        st.markdown('<div class="chat-history">', unsafe_allow_html=True)


        with chat_history:
            for i, chat in enumerate(st.session_state.history):
                st_msg(avatar_style=None, key=f"chat_{i}:", **chat)

        input_text = st.text_input("Please type your queries/message here...", key="input_text", on_change=self.got_msg,
                                   max_chars=200)
        st.markdown('</div>', unsafe_allow_html=True)

        scroll_js = """
                    <script>
                        var chatHistory = document.getElementById("chat-history");
                        chatHistory.scrollTop = chatHistory.scrollHeight;
                    </script>
                    """

        st.markdown(scroll_js, unsafe_allow_html=True)


Main = main()
