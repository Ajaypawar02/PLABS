import os
import requests
from dotenv import load_dotenv
from langchain.llms import OpenAIChat
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import tiktoken
import sys
sys.path.append("./")

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    print(num_tokens)
    return num_tokens




from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# API parameters

# Article type mapping
article_type_mapping = {
    "very short": {"sections": (1, 1), "word_range": (50, 150)},
    "short": {"sections": (4, 5), "word_range": (50,500)},
    "long_form": {"sections": (8, 9), "word_range": (1500, 2500)},
    "general": {"sections": (1, 1), "word_range": (50, 3000)}
}



def generate_article_without_internet(api_params, llm):


    
    template_without_internet = """You are an AI bot who helps users create different types of content, such as tweets, news articles, blog post and more. Write {article_type} of length in the range {word_range} in the language {language} in the {tone} tone given the following description.
    Description : {Description}
    Since the range is provided, choose the length of the {article_type} properly based on the description provided above.""" 

    
    prompt = PromptTemplate(template=template_without_internet, input_variables=list(api_params.keys()))
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    if api_params["article_type"] == "tweet":
        ans=llm_chain.run({"article_type": api_params["article_type"], "word_range": article_type_mapping["very short"]["word_range"], "Description": api_params["Description"], "language": api_params["language"], "tone": api_params["tone"]})
        print(num_tokens_from_string(ans, "cl100k_base"))

    elif api_params["article_type"] == "news report":
        ans=llm_chain.run({"article_type": api_params["article_type"], "word_range": article_type_mapping["long_form"]["word_range"], "Description": api_params["Description"], "language": api_params["language"], "tone": api_params["tone"]})
        print(num_tokens_from_string(ans, "cl100k_base"))

    elif api_params["article_type"] == "email":
        ans=llm_chain.run({"article_type": api_params["article_type"], "word_range": article_type_mapping["short"]["word_range"], "Description": api_params["Description"], "language": api_params["language"], "tone": api_params["tone"]})
        print(num_tokens_from_string(ans, "cl100k_base"))

    else:
        ans=llm_chain.run({"article_type": api_params["article_type"], "word_range": article_type_mapping["general"]["word_range"], "Description": api_params["Description"], "language": api_params["language"], "tone": api_params["tone"]})
        print(num_tokens_from_string(ans, "cl100k_base"))

    list_image = []
    # if api_params["image"]:
    #     list_image = generate_image(ans, api_params)
    return {
        "answer": ans, 
        "image" : list_image
    }

def generate_article_with_internet(api_params, llm):
    template_search = '''Write the single query in 3-7 words according to guven description so that the query can be provided to Google to get the relevant results.
    Description : {Description}'''
    # llm1 = OpenAIChat(temperature=0, model_name="gpt-3.5-turbo-0613", streaming=True)
    prompt_search = PromptTemplate(template=template_search, input_variables=["Description"])
    llm_chain_search = LLMChain(llm=llm, prompt=prompt_search)
    search_context = llm_chain_search.run({"Description": api_params["Description"]})

    print(type(search_context))

    search = GoogleSerperAPIWrapper(hl=api_params["language"], k= 7)
    print(f"get the search content {search_context}")
    search_results = search.run(search_context)
    print(f"Get internet results {search_results}")

  
    template_with_internet = """You are an AI bot who helps users create different types of content, such as tweets, news articles, blog post and more. Write {article_type} of length in the range {word_range} in the language {language} in the {tone} tone, given the following internet search results.
    Internet Search Results : {search_results}
    Since the range is provided, choose the length of the {article_type} properly based on the description provided above.""" 

    
    prompt = PromptTemplate(template=template_with_internet, input_variables=list(api_params.keys()))
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    if api_params["article_type"] == "tweet":
        ans=llm_chain.run({"article_type": api_params["article_type"], "word_range": article_type_mapping["very short"]["word_range"], "search_results": search_results, "language": api_params["language"], "tone": api_params["tone"]})
        print(num_tokens_from_string(ans, "cl100k_base"))

    elif api_params["article_type"] == "news report":
        ans=llm_chain.run({"article_type": api_params["article_type"], "word_range": article_type_mapping["long_form"]["word_range"], "search_results": search_results, "language": api_params["language"], "tone": api_params["tone"]})
        print(num_tokens_from_string(ans, "cl100k_base"))

    elif api_params["article_type"] == "email":
        ans=llm_chain.run({"article_type": api_params["article_type"], "word_range": article_type_mapping["short"]["word_range"], "search_results": search_results, "language": api_params["language"], "tone": api_params["tone"]})
        print(num_tokens_from_string(ans, "cl100k_base"))

    else:
        ans=llm_chain.run({"article_type": api_params["article_type"], "word_range": article_type_mapping["general"]["word_range"], "search_results": search_results, "language": api_params["language"], "tone": api_params["tone"]})
        print(num_tokens_from_string(ans, "cl100k_base"))

    list_image = []
    # if api_params["image"]:
    #     list_image = generate_image(ans)
    return {
        "answer": ans, 
        "image" : list_image
    }

if __name__ == "__main__":
    api_params = {
"model_id": "gpt-4",
"article_type": "tweet",
"target_keyword": "abu dhabi",
"secondary_keyword": ["abu dhabi weather", "abu dhabi attractions", "abu dhabi dining", "abu dhabi shopping", "abu dhabi culture"],
"article_length": "shorter",
"tone": "polite",
"language": "en",
"country": "ae",
"pov": "first person",
"use_internet": False,
"create_outline": True,
"include_faq": True,
"include_key_takeaways": True,
"streaming": False, 
"auto_link" : True, 
"image" : True
}
    llm = OpenAIChat(temperature=0.9, model_name="gpt-4-0125-preview", streaming=True,  callbacks = [StreamingStdOutCallbackHandler()])
    if api_params["use_internet"]:
        print(generate_article_with_internet(api_params, llm))
    else:
        output = generate_article_without_internet(api_params, llm)
