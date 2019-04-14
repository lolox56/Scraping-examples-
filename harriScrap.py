from urllib.request import urlopen
# from bs4 import BeautifulSoup
import re
import string
from collections import Counter


def cleanSentence(sentence):
    sentence = sentence.split(' ')
    sentence = [word.strip(string.punctuation+string.whitespace) for word in sentence]
    sentence = [word for word in sentence if len(word) > 1
                or (word.lower() == 'a' or word.lower() == 'i')]
    return sentence


def cleanInput(content):
    content = content.upper()
    content = re.sub('\n', ' ', content)
    content = bytes(content, 'UTF-8')
    content = content.decode('ascii', "ignore")
    sentences = content.split('. ')
    return [cleanSentence(sentence) for sentence in sentences]
# returns a list of lists. Each element of the list is a list (each sentence) made of cleaned and striped into words.


def getNgramsFromSentence(content, n):
    output = []
    for i in range(len(content)-n+1):
        output.append(content[i:i+n])
    return output
# returns a list of list. Each list element is an n-gram. A 2-gram from each sentence in this case.


def getNgrams(content, n):
    content = cleanInput(content)
    ngrams = Counter()  # An empty collection object. Very easy to use but nice and important.
    ngrams_list = []
    for sentence in content:
        # ' '.join([str1, str2]) results in 'str1 str2'. It joins the 2-grams into single string literals separated by a
        # whitespace. So, expression below generates a list of fused 2-grams if none of the words making up a 2-gram is
        # a commonWord.
        newNgrams = [' '.join(ngram) for ngram in getNgramsFromSentence(sentence, 2) if isCommon(ngram) is False]
        ngrams_list.extend(newNgrams)
        ngrams.update(newNgrams)  # updates the collection object.
    return ngrams


def isCommon(ngram):
    commonWords = ['THE', 'BE', 'AND', 'OF', 'A', 'IN', 'TO', 'HAVE', 'IT', 'I',
                   'THAT', 'FOR', 'YOU', 'HE', 'WITH', 'ON', 'DO', 'SAY', 'THIS', 'THEY',
                   'IS', 'AN', 'AT', 'BUT', 'WE', 'HIS', 'FROM', 'THAT', 'NOT', 'BY',
                   'SHE', 'OR', 'AS', 'WHAT', 'GO', 'THEIR', 'CAN', 'WHO', 'GET', 'IF',
                   'WOULD', 'HER', 'ALL', 'MY', 'MAKE', 'ABOUT', 'KNOW', 'WILL', 'AS',
                   'UP', 'ONE', 'TIME', 'HAS', 'BEEN', 'THERE', 'YEAR', 'SO', 'THINK',
                   'WHEN', 'WHICH', 'THEM', 'SOME', 'ME', 'PEOPLE', 'TAKE', 'OUT', 'INTO',
                   'JUST', 'SEE', 'HIM', 'YOUR', 'COME', 'COULD', 'NOW', 'THAN', 'LIKE',
                   'OTHER', 'HOW', 'THEN', 'ITS', 'OUR', 'TWO', 'MORE', 'THESE', 'WANT',
                   'WAY', 'LOOK', 'FIRST', 'ALSO', 'NEW', 'BECAUSE', 'DAY', 'MORE', 'USE',
                   'NO', 'MAN', 'FIND', 'HERE', 'THING', 'GIVE', 'MANY', 'WELL']
    for word in ngram:
        if word in commonWords:
            return True
    return False


content = str(urlopen('http://pythonscraping.com/files/inaugurationSpeech.txt').read(), 'utf-8')
ngrams = getNgrams(content, 2)
print(ngrams)