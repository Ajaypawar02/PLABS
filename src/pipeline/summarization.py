import os
from typing import Dict
import logging
import os
import openai
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAIChat
from langchain.text_splitter import TokenTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


text = "string"




class Summarization:
    def __init__(self, model):
        self.llm= OpenAIChat(temperature=0.9, model_name= model, streaming=True,  callbacks = [StreamingStdOutCallbackHandler()])
        self.embeddings = OpenAIEmbeddings()

    def summarize(self, input_text: str) -> str:
        text_splitter = TokenTextSplitter(chunk_size=3500, chunk_overlap=0)
        texts = text_splitter.split_text(input_text)

        prompt_template = """
        Please summarize the following text:

        {context}

        Summary:
        """

        prompt = PromptTemplate(
            input_variables=["context"],
            template=prompt_template,
        )


        chain = LLMChain(llm=self.llm, prompt=prompt, verbose=False)
        count = 0
        summaries = []
        for chunk in texts:
            count += 1
            summary = chain.run(context=chunk)
            summaries.append(summary)
            logging.info(f"API is called {count} number of times and, Summary of part {count} : {summary}")

        combined_summary = " ".join(summaries)

        bullet_points_prompt = """
        Please generate 2-3 bullet points that summarize the key points from the following text:

        {summary}

        Bullet points:
        """

        bullet_points_prompt_template = PromptTemplate(
            input_variables=["summary"],
            template=bullet_points_prompt,
        )
        
        bullet_points_chain = LLMChain(llm=self.llm, prompt=bullet_points_prompt_template)
        bullet_points = bullet_points_chain.run(summary=combined_summary)

        return bullet_points
    
       