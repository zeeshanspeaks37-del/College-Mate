from google import genai
from dotenv import load_dotenv
import os

from rag import load_knowledge, create_chunks, search_knowledge


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Load SJEC knowledge
text = load_knowledge()
chunks = create_chunks(text)


# Student question
question = "What is the examination section phone number?"


# Search the SJEC knowledge
results = search_knowledge(question, chunks)


# Combine the search results
context = "\n\n".join(results)


# Ask Gemini using the retrieved information
prompt = f"""
You are College Mate, an AI assistant for St Joseph Engineering College (SJEC).

Answer the student's question using ONLY the college information provided below.

If the information is not available, say:
"I don't have that information in my current college knowledge base."

Do not invent information.

COLLEGE INFORMATION:
{context}

STUDENT QUESTION:
{question}
"""


interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt
)


print("\nCollege Mate:")
print(interaction.output_text)