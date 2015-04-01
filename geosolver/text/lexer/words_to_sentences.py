__author__ = 'minjoon'

def words_to_sentences(words):
    sentences = []
    sentence = {}
    punctuations = ".?!"
    idx = 0
    for word in words:
        sentence[idx] = word
        if word in punctuations:
            sentences.append(sentence)
            sentence = {}
            idx = 0
        else:
            idx += 1
    if len(sentence) > 0:
        sentences.append(sentence)
    return sentences
