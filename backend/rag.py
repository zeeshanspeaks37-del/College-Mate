from pathlib import Path


def load_knowledge():
    file_path = Path(__file__).parent.parent / "knowledge" / "sjec_info.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


def create_chunks(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def search_knowledge(question, chunks):
    question_words = question.lower().split()

    # Common words that do not help much with knowledge retrieval
    stop_words = {
        "what", "is", "the", "a", "an", "of",
        "to", "for", "in", "on", "at", "and",
        "does", "do", "can", "i", "my", "me",
        "where", "when", "who", "how", "are",
        "was", "were", "will", "would", "could",
        "should", "this", "that", "it", "tell",
        "about", "please", "there", "from",
        "which", "with", "be", "has", "have"
    }

    # Clean the question and keep meaningful words
    important_words = []

    for word in question_words:
        cleaned_word = word.strip(".,?!:;()[]{}\"'")

        if cleaned_word and cleaned_word not in stop_words:
            important_words.append(cleaned_word)

    # If the question contains no meaningful words,
    # there is not enough information to search.
    if not important_words:
        return []

    results = []

    for chunk in chunks:

        chunk_lower = chunk.lower()

        score = 0
        matched_words = []

        for word in important_words:

            if word in chunk_lower:
                score += 1
                matched_words.append(word)

        if score > 0:
            results.append(
                (score, len(matched_words), chunk)
            )

    # No matching information
    if not results:
        return []

    # Sort by relevance score
    results.sort(
        reverse=True,
        key=lambda x: (x[0], x[1])
    )

    best_score = results[0][0]

    # ---------------------------------------------
    # RELEVANCE CHECK
    # ---------------------------------------------
    #
    # For short questions:
    # One strong matching word can sometimes be enough.
    #
    # For longer questions:
    # Require at least two meaningful matching words.
    #

    if len(important_words) >= 4:

        if best_score < 2:
            return []

    elif len(important_words) >= 2:

        if best_score < 1:
            return []

    else:

        if best_score < 1:
            return []

    # ---------------------------------------------
    # RETURN TOP RELEVANT CHUNKS
    # ---------------------------------------------

    return [
        chunk
        for score, matched_count, chunk in results[:3]
    ]


if __name__ == "__main__":

    text = load_knowledge()

    chunks = create_chunks(text)

    print("Knowledge loaded successfully!")
    print(f"Number of chunks: {len(chunks)}")

    print("\n----------------------------------------")
    print("Testing College Mate Knowledge Search")
    print("----------------------------------------")

    test_questions = [
        "What scholarship opportunities are available at SJEC?",
        "Who is the CSE HOD?",
        "Where is the library?",
        "What is Earth?",
        "What is a sunset?",
        "Who is Elon Musk?"
    ]

    for question in test_questions:

        print(f"\nQuestion: {question}")

        results = search_knowledge(
            question,
            chunks
        )

        if not results:

            print("Result: No relevant college information found.")

        else:

            print(f"Result: {len(results)} relevant chunk(s) found.")

            for result in results:

                print("\n---")
                print(result[:500])