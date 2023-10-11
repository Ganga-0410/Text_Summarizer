from flask import Flask, render_template, request
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from googletrans import Translator

app = Flask(__name__)

def calculate_word_frequencies(sentence_list):
    word_frequencies = {}
    stop_words = set(stopwords.words("english"))

    for word in sentence_list:
        if word.lower() not in stop_words:
            if word.lower() not in word_frequencies.keys():
                word_frequencies[word.lower()] = 1
            else:
                word_frequencies[word.lower()] += 1

    return word_frequencies

def calculate_sentence_scores(sentences, word_frequencies):
    sentence_scores = {}

    for sentence in sentences:
        for word, freq in word_frequencies.items():
            if word in sentence.lower():
                if sentence not in sentence_scores.keys():
                    sentence_scores[sentence] = freq
                else:
                    sentence_scores[sentence] += freq

    return sentence_scores    # ... (previous code remains the same)

def generate_summary(text, num_sentences, target_lang):
    translator = Translator()

    if target_lang != 'en':
        translation = translator.translate(text, src='en', dest=target_lang)
        text = translation.text

    sentences = sent_tokenize(text)
    word_list = word_tokenize(text)

    word_frequencies = calculate_word_frequencies(word_list)
    sentence_scores = calculate_sentence_scores(sentences, word_frequencies)

    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)

    summary_sentences = [sentence[0] for sentence in sorted_sentences[:num_sentences]]

    return ' '.join(summary_sentences)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary', methods=['POST'])
def summary():
    user_input = request.form['user_input']
    target_lang = request.form['target_lang']
    summary = generate_summary(user_input, num_sentences=3, target_lang=target_lang)
    return render_template('summary.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
