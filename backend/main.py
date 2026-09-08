from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os

from backend.rag import (
    load_knowledge,
    create_chunks,
    search_knowledge
)


# ---------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------

load_dotenv()


# ---------------------------------------------
# CREATE FASTAPI APP
# ---------------------------------------------

app = FastAPI()


# ---------------------------------------------
# CONNECT TO GEMINI
# ---------------------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ---------------------------------------------
# LOAD COLLEGE KNOWLEDGE
# ---------------------------------------------

text = load_knowledge()

chunks = create_chunks(text)


# ---------------------------------------------
# QUESTION MODEL
# ---------------------------------------------

class Question(BaseModel):
    question: str


# ---------------------------------------------
# COLLEGE MATE FRONTEND
# ---------------------------------------------

@app.get("/")
def home():

    frontend_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "frontend",
        "index.html"
    )

    return FileResponse(frontend_path)


# ---------------------------------------------
# ASK COLLEGE MATE
# ---------------------------------------------

@app.post("/ask")
def ask_college_mate(data: Question):

    question = data.question.strip()


    # -----------------------------------------
    # EMPTY QUESTION CHECK
    # -----------------------------------------

    if not question:

        return {
            "answer":
            "Please enter a question related to St Joseph Engineering College."
        }


    # -----------------------------------------
    # SEARCH COLLEGE KNOWLEDGE BASE
    # -----------------------------------------

    results = search_knowledge(
        question,
        chunks
    )


    # -----------------------------------------
    # UNKNOWN / OUT-OF-SCOPE QUESTION
    # -----------------------------------------

    if not results:

        return {
            "answer":
            "I couldn't find reliable information about that in my current college knowledge base. I can help you with information related to St Joseph Engineering College."
        }


    # -----------------------------------------
    # COMBINE RETRIEVED INFORMATION
    # -----------------------------------------

    context = "\n\n".join(results)


    # -----------------------------------------
    # AI PROMPT
    # -----------------------------------------

    prompt = f"""
You are College Mate, an AI assistant for
St Joseph Engineering College (SJEC).

Your job is to answer questions about the college
using ONLY the college information provided below.

STRICT RULES:

1. Use ONLY the provided college information.

2. Do NOT use your general world knowledge to answer
   the student's question.

3. Do NOT invent names, dates, locations, events,
   phone numbers, departments, results, or any other
   information.

4. If the student's question is unrelated to
   St Joseph Engineering College, do NOT answer it.

5. If the student's question is related to the college
   but the answer cannot be found in the provided
   information, say:

"I couldn't find that information in my current
college knowledge base."

6. If the retrieved information does not actually
   answer the student's question, use the same
   fallback response.

7. Keep answers clear, useful, and concise.

COLLEGE KNOWLEDGE:

{context}

STUDENT QUESTION:

{question}
"""


    # -----------------------------------------
    # ASK GEMINI
    # -----------------------------------------

    try:

        interaction = client.interactions.create(
            model="gemini-3.1-flash-lite",
            input=prompt
        )


        answer = interaction.output_text.strip()


    except Exception as error:

        print("Gemini error:", error)

        return {
            "answer":
            "Sorry, I couldn't process your question right now. Please try again."
        }


    # -----------------------------------------
    # SAFETY FALLBACK
    # -----------------------------------------

    if not answer:

        answer = (
            "I couldn't find reliable information about "
            "that in my current college knowledge base."
        )


    # -----------------------------------------
    # RETURN ANSWER TO FRONTEND
    # -----------------------------------------

    return {
        "answer": answer
    }