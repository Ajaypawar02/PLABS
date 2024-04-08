import os
from typing import Dict
import logging
import sys
import os
import openai
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAIChat
from langchain.text_splitter import TokenTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
sys.path.append('./')
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")



class SentimentAnalysis:
    def __init__(self, model):
        self.llm = OpenAIChat(temperature=0.9, model_name=model, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
        self.embeddings = OpenAIEmbeddings()

    def sentiment_analysis(self, input_text:str) -> Dict:
        
        prompt= '''You are an expert English linguist. Perform sentiment analysis on the given context and assign one of the labels = [positive, negative, neutral].

Context : {input_text}

Constraints: First generate the label with the delimiter “Sentiment Label” and then generate the sentiment rating in the range of 0 to 100 percentage to the given context with the delimiter “Sentiment Rating”.\n\n'''        
        prompt_template = PromptTemplate.from_template(prompt)
        llm_chain = LLMChain(llm=self.llm, prompt=prompt_template, verbose=False)
        response = llm_chain.run({'input_text': input_text})
        print(response)
        return {'response': response}