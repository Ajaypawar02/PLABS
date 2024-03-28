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
    "shorter": {"sections": (2, 3), "word_range": (450, 900)},
    "short": {"sections": (4, 5), "word_range": (900, 1350)},
    "medium": {"sections": (6, 7), "word_range": (1350, 1800)},
    "long_form": {"sections": (8, 9), "word_range": (1800, 2350)},
    "longer": {"sections": (10, 12), "word_range": (2350, 2940)}
}



def generate_article_without_internet(api_params, llm):
    selected_type = api_params["article_length"]
    sections, word_range = article_type_mapping[selected_type]["sections"], article_type_mapping[selected_type]["word_range"]


    
    template_without_internet = """You are an AI bot who helps users create different types of content, such as blog posts, product reviews, and more. Write {article_type} article of length {word_range} words with {sections} sections (H2, H3, H4) on the topic '{target_keyword}' including secondary keywords {secondary_keyword} in {tone} tone for a {country} audience in {language} language and {pov} point of view. Addiitonally create an outline, include FAQ and key takeaways if true respectively.
    create_outline: {create_outline}, include_faq: {include_faq}, include_key_takeaways: {include_key_takeaways}."""


    prompt = PromptTemplate(template=template_without_internet, input_variables=list(api_params.keys()))
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    ans=llm_chain.run({"article_type": api_params["article_type"], "word_range": word_range, "sections": sections, "target_keyword": api_params["target_keyword"], "secondary_keyword": api_params["secondary_keyword"], "tone": api_params["tone"], "language": api_params["language"], "country": api_params["country"], "pov": api_params["pov"], "create_outline": api_params["create_outline"], "include_faq": api_params["include_faq"], "include_key_takeaways": api_params["include_key_takeaways"]})
    print(num_tokens_from_string(ans, "cl100k_base"))

    list_image = []
    # if api_params["image"]:
    #     list_image = generate_image(ans, api_params)
    return {
        "answer": ans, 
        "image" : list_image
    }

def generate_article_with_internet(api_params, llm):
    selected_type = api_params["article_length"]
    sections, word_range = article_type_mapping[selected_type]["sections"], article_type_mapping[selected_type]["word_range"]
    template_search = "Using the target keyword '{target_keyword}' and secondary keywords {secondary_keyword} and article type {article_type} write a single query for an internet search not more than 4 words."
    # llm1 = OpenAIChat(temperature=0, model_name="gpt-3.5-turbo-0613", streaming=True)
    prompt_search = PromptTemplate(template=template_search, input_variables=["target_keyword", "secondary_keyword"])
    llm_chain_search = LLMChain(llm=llm, prompt=prompt_search)
    search_context = llm_chain_search.run({"article_type": api_params["article_type"], "target_keyword": api_params["target_keyword"], "secondary_keyword": api_params["secondary_keyword"]})

    print(type(search_context))

    search = GoogleSerperAPIWrapper(gl=api_params["country"], hl=api_params["language"], k= 7)
    print(f"get the search content {search_context}")
    search_results = search.run(search_context)
    print(f"Get internet results {search_results}")

  
    template_with_internet = """You are an AI bot who helps users create different types of content, such as blog posts, product reviews, and more. Write an article of length {word_range}  words with {sections} sections (H2, H3, H4) on the topic '{target_keyword}' including secondary keywords {secondary_keyword} in {tone} tone for a {country} audience in {language} language and {pov} point of view based on internet search results {answer}. Create an outline, include FAQ and key takeaways if specified.
        create_outline: {create_outline}, include_faq: {include_faq}, include_key_takeaways: {include_key_takeaways}.
        Guidelines- When writing, focus on complexity and mixing short and long sentences, like a human writer. Use unique words for freshness. Keep the tone professional and original, avoiding common AI phrases. Apply "Pharical Magic" by using easy yet unique words, and change every usual word to a unique or simpler synonym or antonym, including similes for interest.
    """

    prompt = PromptTemplate(template=template_with_internet, input_variables=list(api_params.keys()) + ["answer"])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    ans=llm_chain.run({"word_range": word_range, "sections": sections, "target_keyword": api_params["target_keyword"], "secondary_keyword": api_params["secondary_keyword"], "tone": api_params["tone"], "language": api_params["language"], "country": api_params["country"], "pov": api_params["pov"], "create_outline": api_params["create_outline"], "include_faq": api_params["include_faq"], "include_key_takeaways": api_params["include_key_takeaways"], "answer": search_results})
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
