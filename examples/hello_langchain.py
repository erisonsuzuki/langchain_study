import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Set up the model
# By default, it uses the OPENAI_API_KEY environment variable
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 2. Create a prompt template
# This will guide the model's response
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world-class comedian."),
    ("user", "Tell me a joke about {topic}.")
])

# 3. Create a simple chain
# This pipes the components together:
# prompt -> llm -> output_parser
chain = prompt | llm | StrOutputParser()

# 4. Run the chain
# The input to the chain is a dictionary that fills the prompt's variables
topic = "a developer"
response = chain.invoke({"topic": topic})

print(f"Joke about {topic}:")
print(response)

# Example Output:
# Joke about a developer:
# Why do developers prefer dark mode?
# Because light attracts bugs!
