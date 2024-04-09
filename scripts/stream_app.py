import streamlit as st
import requests
from PIL import Image
import base64

# Define FastAPI endpoint URLs
GENERATE_ARTICLE_URL = "http://localhost:7000/generate_article"
SUMMARIZATION_URL = "http://localhost:7000/generate_summary"
NER_URL = "http://localhost:7000/NER"
SENTIMENT_URL = "http://localhost:7000/sentiment_analysis"
CLASSIFICATION_URL = "http://localhost:7000/classification"
# Streamlit UI
st.title("FastAPI Integration with Streamlit")

# Function to call FastAPI endpoint
def call_api(endpoint, data):
    response = requests.post(endpoint, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error calling API: {response.status_code}")

def call_api_image(endpoint, data):
    response = requests.post(endpoint, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error calling API: {response.status_code}")
        

def decode_base64_image(base64_string):
    return Image.open(base64_string)

def display_base64_image(base64_str):
    # If your string has a prefix, remove it (e.g., "data:image/png;base64,")
    if "base64," in base64_str:
        base64_str = base64_str.split("base64,")[-1]
    
    # Decode the Base64 string
    image_bytes = base64.b64decode(base64_str)
    
    # Convert bytes data to a PIL Image and display it
    st.image(image_bytes, use_column_width=True)

# Streamlit components
option = st.sidebar.selectbox("Select Action", ["Generation", "Summarization", "NER"]) #"Sentiment Analysis", "Classification"])

if option == "Generation":
    st.subheader("Generate Article")

    # Define options for selectbox fields
    model_options = ["gpt-4-0125-preview", "gpt-3.5-turbo-0125"]  
    article_type_options = ["news report","tweet", "email"]
    tone_options = ["polite","SEO Optimized (confident, knowledgeable, neutral, and clear)","Excited" ,"Professional", "Friendly", "Formal", "Casual", "Humorous"]
   
    language_options = ["en", "Czech"]  # Add more languages as needed  # Add more countries as needed
   
    # Input components for each field
    model_id = st.selectbox("Model ID", model_options)
    article_type = st.selectbox("Article Type", article_type_options)
    tone = st.selectbox("Tone", tone_options)
    if article_type == "news report":

        Description = st.text_input("Description", value = "")

        
        language = st.selectbox("Language", language_options)
        
        use_internet = st.checkbox("Use Internet", value=False)
        # create_outline = st.checkbox("Create Outline", value=True)
        # include_faq = st.checkbox("Include FAQ", value=False)
        # include_key_takeaways = st.checkbox("Include Key Takeaways", value=True)
        # streaming = st.checkbox("Streaming", value=True)
        # auto_link = st.checkbox("Auto Link", value=False)
        # image = st.checkbox("Image", value=False)
        # image = st.checkbox("Include Image", value=False)
        
        if st.button("Generate"):
                # Prepare data based on user inputs

                
                    
            data = {
                "model_id": model_id,
                "article_type": article_type,
                "Description": Description,
                "tone": tone,
                "language": language,

                "use_internet": use_internet,
                
            }

            print(data)
        
            # Call FastAPI endpoint
            result = call_api(GENERATE_ARTICLE_URL, data)
            data_image = {
                "text": result["answer"]
            }
            # Display response
            st.write(f'Generated {article_type}')
            st.markdown(result["answer"]) 
            data_link = {
                "article" : result["answer"]
            }
        
    else:
        Description = st.text_input("Description", value = "")

        
        language = st.selectbox("Language", language_options)
            
            # create_outline = st.checkbox("Create Outline", value=True)
            # include_faq = st.checkbox("Include FAQ", value=False)
            # include_key_takeaways = st.checkbox("Include Key Takeaways", value=True)
            # streaming = st.checkbox("Streaming", value=True)
            # auto_link = st.checkbox("Auto Link", value=False)
            # image = st.checkbox("Image", value=False)
            # image = st.checkbox("Include Image", value=False)
            
        if st.button("Generate"):
                    # Prepare data based on user inputs

                    
                        
            data = {
                    "model_id": model_id,
                    "article_type": article_type,
                    "Description": Description,
                    
                    "language": language,

                    "use_internet": False,
                    
                }

            print(data)
            
                # Call FastAPI endpoint
            result = call_api(GENERATE_ARTICLE_URL, data)
            data_image = {
                    "text": result["answer"]
                }
                # Display response
            st.write(f'Generated {article_type}')
            st.markdown(result["answer"]) 
            data_link = {
                    "article" : result["answer"]
                }
            # st.markdown(image["image"])
            
        # display_base64_image(image["image"][0])

if option == "Summarization":
    st.subheader("Provide the input data below : ")
    article = st.text_area("Article")
    model_options = ["gpt-4-0125-preview", "gpt-3.5-turbo-0125"]  
    model_id = st.selectbox("Model ID", model_options)

    if st.button("Generate Summary"):
        data = {"model": model_id, "text": article}
        result = call_api(SUMMARIZATION_URL, data)
        st.write("Response:")
        st.markdown(result['summary'])

if option == "NER":
    st.subheader("Named Entity Recognition")
    text = st.text_area("Enter text")
    comma_text = st.text_area("Enter comma separated text")
    model_options = ["gpt-4-0125-preview", "gpt-3.5-turbo-0125"]  
    model_id = st.selectbox("Model ID", model_options)

    if st.button("Generate"):
        data = {"model": model_id, "text": text, "comma_text": comma_text}
        result = call_api(NER_URL, data)
        st.write("Response:")
        st.markdown(result['response'])

# if option == "Sentiment Analysis":
#     st.subheader("Sentiment Analysis")
#     model_options = ["gpt-4-0125-preview", "gpt-3.5-turbo-0125"]  
#     text = st.text_area("Enter text")
#     model_id = st.selectbox("Model ID", model_options)

#     if st.button("Generate"):
#         data = {"model": model_id, "text": text}
#         result = call_api(SENTIMENT_URL, data)
#         st.write("Response:")
#         st.markdown(result['response'])

# if option == "Classification":
#     st.subheader("Classification")
#     text = st.text_area("Enter text")
#     model_options = ["gpt-4-0125-preview", "gpt-3.5-turbo-0125"]  
#     model_id = st.selectbox("Model ID", model_options)
#     topic_options = ["topic detection", "news", "sentiment analysis"]
#     topic = st.selectbox("Topic", topic_options)

#     if st.button("Generate"):
#         data = {"model": model_id, "text": text, "topic": topic}
#         result = call_api(CLASSIFICATION_URL, data)
#         st.write("Response:")
#         st.markdown(result['response'])