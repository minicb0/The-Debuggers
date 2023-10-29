import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

file_path = 'scraped_data.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    scraped_data = file.read()

sentences = sent_tokenize(scraped_data)

words = word_tokenize(scraped_data)

stop_words = set(stopwords.words('english'))
filtered_words = [word for word in words if word.lower() not in stop_words]

fdist = FreqDist(filtered_words)
most_common_words = fdist.most_common(10)

insights = "Top 10 most common words:\n"
for word, frequency in most_common_words:
    insights += f"{word}: {frequency} times\n"

with open('insights.txt', 'w', encoding='utf-8') as file:
    file.write(insights)

print("Insights extracted and saved to 'insights.txt'.")

