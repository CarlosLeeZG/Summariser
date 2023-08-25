# Imports the OpenAI API and Streamlit libraries.
# import pip_system_certs.wrapt_requests
import streamlit as st
import os
from langchain.document_loaders import UnstructuredFileIOLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import AzureChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from typing import Dict, Any, List
from langchain.callbacks.base import BaseCallbackHandler
from langchain.docstore.document import Document
import re
import io


class ProgressBarHandler(BaseCallbackHandler):
    current_counter = 0
    total_counter = 1
    progress_bar = None
    def __init__(
        self,
        total_counter=1
    ) -> None:
        self.total_counter = total_counter
        self.progress_bar = st.progress(0, text=f"Total chunks: {str(total_counter)}")
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        self.current_counter += 1
        self.progress_bar.progress(int((self.current_counter * 1.0 / (self.total_counter + 1)) * 100))






def main():

    openai_token = os.environ.get("OPENAI_TOKEN", "")
    openai_endpoint = "https://mti-nerve-openai-jp-east.openai.azure.com/"
        

        

    
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = "2023-05-15"
    os.environ["OPENAI_API_BASE"] = openai_endpoint
    os.environ["OPENAI_API_KEY"] = "5d15498f2d0f4bbfa507c01fb859912e"





    
    if check_password():

        # Set page title
        st.set_page_config(page_title="Document Summarizer")

        # Add a title
        st.title("Document Summarizer")

        max_summary_size = st.number_input('Max summary words(Indicative)', value=200, step=1, min_value=50)

        # Add a file uploader widget
        uploaded_file = st.file_uploader("Choose a file")

        # Check if a file was uploaded
        if uploaded_file is not None:
            file = io.BytesIO(uploaded_file.read())
            
            # Read the contents of the file
            loader = UnstructuredFileIOLoader(file)
            documents = loader.load()
            llm = AzureChatOpenAI(temperature=0, 
                verbose=True, 
                deployment_name="gpt-35-turbo-16k"
            )
            chain = load_summarize_chain(llm, chain_type="refine")

            splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=8000, chunk_overlap=20)


            split_documents = splitter.split_documents(documents)

            handler = ProgressBarHandler(total_counter=len(split_documents))
            summarize_text = chain.run(split_documents, callbacks=[handler])

            current_tries = 1
            
            while len(re.findall(r'\w+', summarize_text)) > max_summary_size and current_tries <= 5:
                split_texts = splitter.split_text(summarize_text)
                split_documents = [Document(page_content=t) for t in split_texts]
                summarize_text = chain.run(split_documents)
                current_tries += 1

            st.write(str(summarize_text))





def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if __name__ == "__main__":
    main()
