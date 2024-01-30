import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey, act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analysis,
and big data engineering. Your task is to evaluate the resume based on the given job description.
Consider that the job market is very competitive, and you should provide 
the best assistance for improving the resumes. Assign the percentage matching based 
on JD and
the missing keywords with high accuracy.
Resume: {text}
Description: {jd}

I want the response in one single string having the structure
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""
 
# Streamlit app
st.set_page_config(
    page_title="Smart ATS",
    page_icon="✨",
    layout="wide"
) 
st.title("Smart ATS Tracking System")
st.markdown(":dart: Elevate your hiring game! This Smart ATS system effortlessly analyzes resumes, delivering a quick percentage match and highlighting missing keywords. Simplify your recruitment journey.")
jd = st.text_area(":gray[Paste the Job Description]", height=150)
 
uploaded_file = st.file_uploader(":gray[Upload Your Resume :red[(PDF)]]", type="pdf", help="Please upload the PDF")
 
submit = st.button("Submit")
 
if submit and uploaded_file:
    st.markdown("---") 
 
    text = input_pdf_text(uploaded_file)
    response = get_gemini_response(input_prompt.format(text=text, jd=jd))
 
    try:
        
        response_dict = eval(response)
        st.subheader(f":rainbow[JD Match:] {response_dict.get('JD Match', 'N/A')}") 
        st.caption('Jd Match should be above 75%')
        st.subheader(":rainbow[Missing Keywords:]")
        st.write(response_dict.get("MissingKeywords", []))

        st.subheader(":rainbow[Profile Summary:]")
        st.write(response_dict.get("Profile Summary", "N/A"))

    except Exception as e:
        st.error(f"Error processing the response: {e}")
 

# Add a footer 
st.divider()
st.markdown("Created with :red[❤️] by :rainbow[Rohit Yadav]")