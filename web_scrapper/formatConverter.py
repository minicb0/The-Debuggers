def preprocess_text(text):
    return text.replace('"', "'")

with open('input.txt', 'r') as input_file, open('output.txt', 'w') as output_file:
    question = None
    answer = None

    for line in input_file:
        line = line.strip()

        if line.startswith('Q:'):
            question = preprocess_text(line[3:].strip())
        elif line.startswith('A:'):
            answer = preprocess_text(line[3:].strip())
            if question is not None and answer is not None:
                output_file.write(f'("{question}", "{answer}"),\n')
                question = None
                answer = None
