from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Set the Poppler path explicitly
poppler_path = r'E:\Downloads\Release-23.11.0-0\poppler-23.11.0\Library\bin'

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image 
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App
st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Main Content Styling
 

# Main Content
st.title("Resume Analysis App")

# Job Description Input
input_text = st.text_area("Enter Job Description:", key="input")

# Upload Resume
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

# Buttons Styling
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }
        .stButton:hover>button { 
            color: white; 
            border-color: #4caf50;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Buttons
col1, col2 = st.columns(2)

with col1:
    submit1 = st.button("Tell Me About the Resume", key="tell_me_button")
    input_prompt1 = """
    You are an experienced HR with tech experience in the field of any one job role from Full stack
    Web development, Data Science, DEVOPS. Your task is to review the provided resume against the job description for these profiles.
    Please share your professional evaluation on whether the candidate's profile aligns with the role.
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """ 
    st.markdown("<small><i>Tip: Click the button to analyze the resume.</i></small>", unsafe_allow_html=True)

with col2:
    submit3 = st.button("Percentage Match", key="percentage_match_button")
    input_prompt3 = """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from Full stack Web development, Data Science, DEVOPS, and ATS functionality. Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
    the job description. First, the output should come as a percentage, and then keywords missing, and last final thoughts.
    """
    st.markdown("<small><i>Tip: Click the button to calculate the percentage match.</i></small>", unsafe_allow_html=True)

# Button Actions
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Analysis Result:")
        st.write(response)
    else:
        st.warning("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Analysis Result:")
        st.write(response)
    else:
        st.warning("Please upload the resume")
