##  health management app
from dotenv import load_dotenv

load_dotenv()   ## load all the environment variables


import streamlit as st
import os
import google.generativeai as genai
from PIL import Image



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Google Pro Vision API And get response

def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def imput_image_setup(uploaded_file):
    #check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into Bytes
        bytes_data= uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of uploaded file
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

## initialize our stream app
st.set_page_config(page_title="Gemini health App")
st.header("Gemini Health App")
input=st.text_input("Input Prompt:", key="input")
uploaded_file=st.file_uploader("choose an image...", type=["jpg","jpeg","png"])

image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="uploaded Image.",use_column_width=True)

submit=st.button("tell me the total calaries ")
input_prompt="""
you are an expert in nutritionist where you need to see the food items from the image
and calculate the total calaories, also provide the details of every food items with calaories intake
is below format

1. Item 1 - no of calaries
2. Item 2 - no of calaries
----
----

"""

## if submit button is clicked
if submit:
    image_data=imput_image_setup(uploaded_file) 
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("the response is")
    st.write(response)





