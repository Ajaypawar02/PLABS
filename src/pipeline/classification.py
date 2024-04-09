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

text = '''Last night, I found myself standing amidst of a vast landscape and the ground beneath me felt a mosaic of cracked earth and debris.
As I approached volcano, air grew warmer and scent of sulphur hung heavily around me. 
The earth around me trembled with the volcano's restlessness which was about to unfold, the incandescent lava shot into the sky above me painting it with crimson red and gold. 
Despite the chaos, I was unable to tear my gaze away from the mesmerizing cascaded down slopes of a fiery waterfall (lava), unbearable heat and the liberation of long suppressed emotions.'''


class Classification:
    def __init__(self, model):
        self.llm = OpenAIChat(temperature=0.9, model_name=model, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
        self.embeddings = OpenAIEmbeddings()
    
    def classify(self, input_text:str, user_option) -> Dict:
        
        
        prompt  = '''Given the input text: {input_text} and the user option of {user_option}:

If the user option is "news", classify the type of news into categories such as "sports", "politics", "technology", etc.

If the user option is "sentiment analysis", determine the sentiment of the input text as "positive", "negative", or "neutral".

If the user option is "topic detection", identify the main topic or topics covered in the input text, such as "environmental issues", "healthcare advancements", "economic trends", etc..

Constraint: Answer in at most 5 words.
'''
        temp_dict = {'input_text': input_text, 'user_option': user_option}
        
        prompt_template = PromptTemplate.from_template(prompt)
        llm_chain = LLMChain(llm=self.llm, prompt=prompt_template, verbose=False)
        response = llm_chain.run(temp_dict)
        return {'response': response}

# ner = Ner("gpt-4-0125-preview")
# input_text = str(input("Enter the text: "))
# print(ner.named_entity_description(input_text))