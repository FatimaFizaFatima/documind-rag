from app.service.rag_service import answer_question

def test_answer_question_relevant():
    result = answer_question("What role does Shintoism play in Ghibli films?")
    print("Answer:", result["answer"])
    print("Sources:", result["sources"])
    assert len(result["sources"]) > 0

def test_answer_question_fallback():
    result = answer_question("What is the best pizza topping?")
    print("Fallback answer:", result["answer"])
    assert result["sources"] == []

if __name__ == "__main__":
    test_answer_question_relevant()
    test_answer_question_fallback()