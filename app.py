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

# Main content
st.title("Smart ATS")

# Job Description Input
jd = st.text_area("Paste the Job Description", height=150)

# Upload Resume
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload the PDF")

# Submit Button
submit = st.button("Submit")

# Result Section
if submit and uploaded_file:
    st.markdown("---") 

    # Analyzing Resume and Generating Response
    text = input_pdf_text(uploaded_file)
    response = get_gemini_response(input_prompt.format(text=text, jd=jd))

    # Displaying Response
    try:
        response_dict = eval(response)
        st.subheader(f"JD Match: {response_dict.get("JD Match")}")
        st.write("A JD Matach of 75% and above is considered as good")

        st.subheader("Missing Keywords:")
        st.write(response_dict.get("MissingKeywords", []))

        st.subheader("Profile Summary:")
        st.write(response_dict.get("Profile Summary", "N/A"))

    except Exception as e:
        st.error(f"Error processing the response: {e}")
 

# Add a footer 
st.divider()  
st.caption('Created with ❤️ by :blue[Rohit]')