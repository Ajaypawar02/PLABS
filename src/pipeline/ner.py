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


class Ner:
    def __init__(self, model):
        self.llm = OpenAIChat(temperature=0.9, model_name=model, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])
        self.embeddings = OpenAIEmbeddings()
    
    def named_entity_description(self, input_text:str, text) -> Dict:
        entity_string = ""
        elements = input_text.split(",")

        elements_list = [elem.strip() for elem in elements]
        for i in range(1, len(elements_list)+1):
            entity_string += str(i) + ". {entity" + str(i) + "}\n"
        
        prompt  = '''### Context: '''
        prompt+= text+'\n\n'

        prompt+= '''As a master paragraph extractor about any entity, your task is to extract the 3 lines around it from the given context and provide an explanation around given entitites from the given text_para above. Keep the context for every entity not more than 100 words
The entities are mentioned hereby: \n\n'''
        prompt+= entity_string+'\n'
        temp_dict = {}
        for i, row in enumerate(elements, start=1):
            temp_dict[f'entity{i}'] = row
        prompt_template = PromptTemplate.from_template(prompt)
        llm_chain = LLMChain(llm=self.llm, prompt=prompt_template, verbose=False)
        response = llm_chain.run(temp_dict)
        return {'response': response}

# ner = Ner("gpt-4-0125-preview")
# input_text = str(input("Enter the text: "))
# print(ner.named_entity_description(input_text))