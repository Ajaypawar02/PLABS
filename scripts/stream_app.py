import streamlit as st
import requests
from PIL import Image
import base64

# Define FastAPI endpoint URLs
GENERATE_ARTICLE_URL = "http://localhost:7000/generate_article"
SUMMARIZATION_URL = "http://localhost:7000/generate_summary"



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
option = st.sidebar.selectbox("Select Action", ["Generation", "Summarization"])

if option == "Generation":
    st.subheader("Generate Article")

    # Define options for selectbox fields
    model_options = ["gpt-4-0125-preview", "gpt-3.5-turbo-0125"]  
    article_type_options = ["news report","tweet", "email"]
    article_length_options = ["shorter","short","medium", "long_form","longer"]
    tone_options = ["polite","SEO Optimized (confident, knowledgeable, neutral, and clear)","Excited" ,"Professional", "Friendly", "Formal", "Casual", "Humorous"]
    language_options = ["en", "Arabic"]  # Add more languages as needed
    country_options = ["SA", "UAE"]  # Add more countries as needed
    pov_options = ["First Person Plural","First Person Singular","Second Person", "Third Person he, she it, ."]
    # Input components for each field
    model_id = st.selectbox("Model ID", model_options)
    article_type = st.selectbox("Article Type", article_type_options)
    target_keyword = st.text_input("Target Keyword", value="health")
    secondary_keywords_input = st.text_input("Secondary Keywords (comma-separated)", value="")
    secondary_keywords = [keyword.strip() for keyword in secondary_keywords_input.split(",") if keyword.strip()]

    article_length = st.selectbox("Article Length", article_length_options)
    tone = st.selectbox("Tone", tone_options)
    language = st.selectbox("Language", language_options)
    country = st.selectbox("Country", country_options)
    pov = st.selectbox("Point of View",pov_options)
    use_internet = st.checkbox("Use Internet", value=False)
    create_outline = st.checkbox("Create Outline", value=True)
    include_faq = st.checkbox("Include FAQ", value=False)
    include_key_takeaways = st.checkbox("Include Key Takeaways", value=True)
    streaming = st.checkbox("Streaming", value=True)
    auto_link = st.checkbox("Auto Link", value=False)
    image = st.checkbox("Image", value=False)
    # image = st.checkbox("Include Image", value=False)
    
    if st.button("Generate"):
            # Prepare data based on user inputs

            
                
        data = {
            "model_id": model_id,
            "article_type": article_type,
            "target_keyword": target_keyword,
            "secondary_keyword": secondary_keywords,
            "article_length": article_length,
            "tone": tone,
            "language": language,
            "country": country,
            "pov": pov,
            "use_internet": use_internet,
            "create_outline": create_outline,
            "include_faq": include_faq,
            "include_key_takeaways": include_key_takeaways,
            "streaming": streaming,
            "auto_link": auto_link,
            "image": image
        }

    
        # Call FastAPI endpoint
        result = call_api(GENERATE_ARTICLE_URL, data)
        data_image = {
            "text": result["answer"]
        }
        # Display response
        st.write("Generated Article:")
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