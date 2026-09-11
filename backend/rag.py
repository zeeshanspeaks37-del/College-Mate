from pathlib import Path


# ---------------------------------------------------------
# LOAD COLLEGE KNOWLEDGE
# ---------------------------------------------------------

def load_knowledge():
    file_path = (
        Path(__file__).parent.parent
        / "knowledge"
        / "sjec_info.txt"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


# ---------------------------------------------------------
# CREATE KNOWLEDGE CHUNKS
# ---------------------------------------------------------

def create_chunks(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks


# ---------------------------------------------------------
# SEARCH KNOWLEDGE
# ---------------------------------------------------------

def search_knowledge(question, chunks):

    # Convert question to lowercase
    question_words = question.lower().split()

    # -----------------------------------------------------
    # COMMON WORDS TO IGNORE
    # -----------------------------------------------------

    stop_words = {
        "what",
        "is",
        "the",
        "a",
        "an",
        "of",
        "to",
        "for",
        "in",
        "on",
        "at",
        "and",
        "does",
        "do",
        "can",
        "i",
        "my",
        "me",
        "where",
        "when",
        "who",
        "how",
        "are",
        "was",
        "were",
        "will",
        "would",
        "could",
        "should",
        "this",
        "that",
        "it",
        "tell",
        "about",
        "please",
        "there",
        "from",
        "which",
        "with",
        "be",
        "has",
        "have",
        "give",
        "show",
        "find"
    }

    # -----------------------------------------------------
    # RELATED WORDS
    # -----------------------------------------------------

    synonyms = {

        # Winners / competitions
        "winner": [
            "winner",
            "won",
            "champion",
            "winning"
        ],

        "win": [
            "win",
            "won",
            "winner",
            "champion"
        ],

        "champion": [
            "champion",
            "winner",
            "won"
        ],

        # Location
        "location": [
            "location",
            "block",
            "room",
            "floor"
        ],

        # Faculty
        "teacher": [
            "teacher",
            "faculty",
            "professor",
            "lecturer"
        ],

        "faculty": [
            "faculty",
            "teacher",
            "professor",
            "lecturer"
        ],

        # HOD
        "hod": [
            "hod",
            "head",
            "department"
        ],

        # Exams
        "exam": [
            "exam",
            "examination",
            "assessment",
            "internal"
        ],

        "examination": [
            "exam",
            "examination",
            "assessment"
        ],

        # Events
        "event": [
            "event",
            "program",
            "competition",
            "activity"
        ],

        # Tournament
        "tournament": [
            "tournament",
            "competition",
            "championship"
        ],

        # Assignments
        "assignment": [
            "assignment",
            "homework",
            "task"
        ],

        # Deadlines
        "deadline": [
            "deadline",
            "last",
            "date",
            "due"
        ],

        # Library
        "library": [
            "library",
            "books",
            "reading"
        ],

        # Cafeteria
        "canteen": [
            "canteen",
            "cafeteria",
            "food"
        ],

        "cafeteria": [
            "cafeteria",
            "canteen",
            "food"
        ],

        # Sports
        "sports": [
            "sports",
            "sport",
            "athletics",
            "tournament"
        ],

        "sport": [
            "sport",
            "sports",
            "athletics",
            "tournament"
        ],

        # Cricket
        "cricket": [
            "cricket"
        ],

        # Football
        "football": [
            "football",
            "soccer"
        ],

        # Hackathon
        "hackathon": [
            "hackathon",
            "coding",
            "innovation"
        ],

        # Timetable
        "timetable": [
            "timetable",
            "schedule",
            "class"
        ],

        "schedule": [
            "schedule",
            "timetable",
            "class"
        ],

        # Fees
        "fee": [
            "fee",
            "fees",
            "payment",
            "pay"
        ],

        "fees": [
            "fees",
            "fee",
            "payment",
            "pay"
        ],

        # Scholarship
        "scholarship": [
            "scholarship",
            "financial",
            "aid"
        ],

        # Placement
        "placement": [
            "placement",
            "career",
            "recruitment",
            "company"
        ],

        # Internship
        "internship": [
            "internship",
            "intern",
            "training"
        ]
    }

    # -----------------------------------------------------
    # CLEAN QUESTION
    # -----------------------------------------------------

    important_words = []

    for word in question_words:

        cleaned_word = word.strip(
            ".,?!:;()[]{}\"'`"
        )

        if (
            cleaned_word
            and cleaned_word not in stop_words
        ):
            important_words.append(
                cleaned_word
            )

    # If there are no useful words
    if not important_words:
        return []

    # -----------------------------------------------------
    # SEARCH EVERY CHUNK
    # -----------------------------------------------------

    results = []

    for chunk in chunks:

        chunk_lower = chunk.lower()

        score = 0

        matched_words = set()

        # -------------------------------------------------
        # DIRECT + RELATED WORD MATCHING
        # -------------------------------------------------

        for word in important_words:

            # Direct match
            if word in chunk_lower:

                score += 2

                matched_words.add(word)

            # Related word match
            related_words = synonyms.get(
                word,
                []
            )

            for related_word in related_words:

                if related_word in chunk_lower:

                    score += 1

                    matched_words.add(word)

                    break

        # -------------------------------------------------
        # YEAR MATCHING
        # -------------------------------------------------

        for word in important_words:

            if (
                word.isdigit()
                and word in chunk_lower
            ):

                # Years are highly important
                score += 3

                matched_words.add(word)

        # -------------------------------------------------
        # SAVE RELEVANT CHUNK
        # -------------------------------------------------

        if score > 0:

            results.append(
                (
                    score,
                    len(matched_words),
                    chunk
                )
            )

    # -----------------------------------------------------
    # NO RESULTS
    # -----------------------------------------------------

    if not results:
        return []

    # -----------------------------------------------------
    # SORT BY RELEVANCE
    # -----------------------------------------------------

    results.sort(
        reverse=True,
        key=lambda x: (
            x[0],
            x[1]
        )
    )

    # -----------------------------------------------------
    # RETURN TOP 3 CHUNKS
    # -----------------------------------------------------

    return [
        chunk
        for score, matched_count, chunk
        in results[:3]
    ]


# ---------------------------------------------------------
# TEST RAG SEARCH
# ---------------------------------------------------------

if __name__ == "__main__":

    # Load knowledge
    text = load_knowledge()

    # Create chunks
    chunks = create_chunks(text)

    print(
        "Knowledge loaded successfully!"
    )

    print(
        f"Number of chunks: {len(chunks)}"
    )

    print(
        "\n----------------------------------------"
    )

    print(
        "Testing College Mate Knowledge Search"
    )

    print(
        "----------------------------------------"
    )

    # Test questions
    test_questions = [

        "What scholarship opportunities are available at SJEC?",

        "Who is the CSE HOD?",

        "Where is the library?",

        "What is the winner of 2025 cricket tournament?",

        "Who won the 2025 cricket competition?",

        "Tell me about 2026 hackathon",

        "What is the timetable?",

        "Where is the cafeteria?",

        "What is Earth?",

        "What is a sunset?",

        "Who is Elon Musk?"
    ]

    # Run tests
    for question in test_questions:

        print(
            f"\nQuestion: {question}"
        )

        results = search_knowledge(
            question,
            chunks
        )

        if not results:

            print(
                "Result: No relevant college information found."
            )

        else:

            print(
                f"Result: {len(results)} relevant chunk(s) found."
            )

            for result in results:

                print("\n---")

                print(
                    result[:500]
                )