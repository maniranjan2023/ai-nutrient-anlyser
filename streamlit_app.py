import streamlit as st;
import google.generativeai as genai;
import os;
from dotenv import load_dotenv;

load_dotenv()


genai.configure(api_key = os.getenv("GOOGLE_API_KEY"));

def get_gemini_response(input_prompt,image):
    model = genai.GenerativeModel('gemini-pro-vision') // since we deal with image so we use gemini pro vision
    response = model.generate_content([input_prompt,image[0]])
    return response.text


def input_image_setup(uploaded_file):

     #check if a file has been uploaded
     if uploaded_file is not None:
          #READ THE FILE INTO BYTES
          bytes_data = uploaded_file.getvalues()

          image_parts= [
               
               {
                    "mime_type":uploaded_file.type,   #get the mime type of the uploaded file
                    "data":bytes_data
               }
               


          ]

          return image_parts
     
     else:
          raise FileNotFoundError("no file uploaded")
     



#initialize our streamlit app

st.set_page_config(page_title = "Gemini health app")

st.header("gemini health app")
uploaded_file = st.file_uploader("choose an image....", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
     image = Image.open(uploaded_file)
     st.image(image,caption = "uploaded Image",use_column_width = True)


submit = st.button("tell me the total calories")


input_prompt = """you are an expert in nutrionist where you need to see the food items from the image and calculate the total calories, also provide the details of every food items with calories intake in below format 

               1.item 1-no of calories
               2.item 2- no of calories
               -----
               -----

               finally you can also mention whether the food is healthy or not

"""

if submit:
     image_data=input_image_setup(uploaded_file)
     response=get_gemini_response(input_prompt,image_data)
     st.header("the resonse is ")
     st.write(response)

