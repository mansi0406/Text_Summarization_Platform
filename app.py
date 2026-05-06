from typing import Optional
import io
import streamlit as st
from transformers import pipeline
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
import os 
import warnings
warnings.filterwarnings("ignore")

# Function : Fetch text from URL

def fetch_text_from_url(url:str)->str:
    response= requests.get(url,timeout=10)
    soup= BeautifulSoup(response.text,"html.parser")
    paragraphs=[p.get_text() for p in soup.find_all("p")]
    return "\n\n".join(paragraphs)

# functiom : Clean  + Truncate text 

def clean_and_truncate(text:str, max_chars: int= 20000)->str:
    cleaned = " ".join(text.strip().split())
    if len(cleaned) > max_chars:
        cleaned = cleaned[:max_chars] + "..."
    
    return cleaned


def create_pdf(summary: str, title: str = "Summary") -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.ln(4)
    pdf.set_font("Arial", "", 12)
    for paragraph in summary.split("\n"):
        pdf.multi_cell(0, 8, paragraph)
        pdf.ln(1)

    pdf_data = pdf.output(dest="S")
    return pdf_data.encode("latin-1")

class Summarizer:

    def __init__(self, model_name:str = "sshleifer/distilbart-cnn-12-6"):
        self.model_name = model_name
        self.pipeline = pipeline("summarization", model=model_name)

    def summarize(self, text:str, max_length:int=150, min_length:int=40, do_sample:bool=False)->str:
        result = self.pipeline(text,max_length=max_length,min_length=min_length,do_sample=do_sample)
        return result[0].get("summary_text","")
    
# Streamlit UI

def main():
    st.set_page_config(page_title="Text Summarizer App", layout="wide")
    st.title("Text Summarizer App - Python + HuggingFace")
    st.markdown("Summarize text, files and webpages")

    left,right=st.columns([1,2])

    with left:

        input_mode =st.radio("Input Type: ",["Text","File","URL"])
        model_choice = st.selectbox("Model:",
                ["sshleifer/distilbart-cnn-12-6","facebook/bart-large-cnn","t5-small"
        ])

        min_length= st.number_input("Minimum Summary tokens:", min_value=5, max_value=100, value=40)
        max_length= st.number_input("Maximum Summary Tokens:", min_value=10, max_value=2000, value=150)

        do_sample= st.checkbox("Use Sampling (creative summaries)", value=False)

        raw_text: Optional[str]=None
        uploaded_file= None
        url_input:Optional[str]=None
        
        if input_mode=="Text":
            raw_text= st.text_area("Enter text here:", height=250)
        elif input_mode == "File":
            uploaded_file= st.file_uploader("Upload .txt or .md file", type =["txt","md"])

        elif input_mode=="URL":
            url_input= st.text_input("Enter webpage URL");
        
        summarize_btn= st.button("Summarize")

    with right:

        st.subheader("Original Text")
        source_container = st.empty()

        st.subheader("Summary Output")
        summary_container = st.empty()

        if summarize_btn:

            user_input_text= ""

            if input_mode== "Text" and raw_text:
                user_input_text = raw_text

            elif input_mode =="File" and uploaded_file:
                uploaded_bytes = uploaded_file.read()
                try:
                    user_input_text= uploaded_bytes.decode("utf-8")
                except:
                    user_input_text=uploaded_bytes.decode("latin-1")
            
            elif input_mode =="URL" and url_input:
                try:
                    user_input_text = fetch_text_from_url(url_input)
                except Exception as e:
                    st.error(f"Failed to fetch URL: {e}")
                    return
            if not user_input_text.strip():
                st.warning("Please provide valid input.")
                return

            user_input_text = clean_and_truncate(user_input_text)

            source_container.code(user_input_text[:8000])

            if min_length >= max_length:
                st.error("Minimun tokens must be smaller than Maximum tokens: ")
                return
            
            summarizer = Summarizer(model_name= model_choice)

            with st.spinner("Generating Summary..."):
                try:
                    summary_text = summarizer.summarize(
                        user_input_text,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=do_sample
                    )
                except Exception as e:
                    st.error(f"Summarization Failed: {e}")
                    return
                
                if not summary_text.strip():
                    st.warning("The model returned an empty summary, Try reducing minimum tokens or adding more text. ")
                    return

                summary_container.write(summary_text)

                pdf_bytes = create_pdf(summary_text, title="Text Summary")
                st.download_button(
                    label="Download Summary as PDF",
                    data=pdf_bytes,
                    file_name="summary.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()                                   
