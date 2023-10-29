import openai

api_key = "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"

with open("insights.txt", "r", encoding="utf-8") as insights_file:
    insights = insights_file.read()

def generate_questions_and_answers(insights):
    prompt = f"Generate questions and answers from the following insights:\n{insights}\n\nQ:"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n = 3
    )

    return response.choices

questions_and_answers = generate_questions_and_answers(insights)

questions = [qa["text"].split("A:")[0].strip() for qa in questions_and_answers]
answers = [qa["text"].split("A:")[1].strip() for qa in questions_and_answers]

with open("generated_qa.txt", "w", encoding="utf-8") as qa_file:
    for q, a in zip(questions, answers):
        qa_file.write(f"Q: {q}\nA: {a}\n\n")

