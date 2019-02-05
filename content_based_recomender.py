from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import math

'''

Preprocessing
1. Remove stopword 
2. Stemming
''' 
# remove most common word
def Stopword_removal(sentence):
    stopword_factory = StopWordRemoverFactory()
    stopwords = stopword_factory.get_stop_words()
    words = sentence.split()
    output = ""
    for word in words:
        if word not in stopwords:
            output = output +" "+word

    return output

# stemming process
def Stemming(sentence):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    output  = stemmer.stem(sentence)
    return output

def Tokenizing(sentence) :
    words = sentence.split()
    tokens = {}
    for word in words:
        try:
            tokens[word] = tokens[word]  + 1
        except KeyError:
            tokens[word] = 1

    return tokens

# preprocessing , remove stopword and stemming process
def Preprocessing(sentence):
    sentence = Stopword_removal(sentence)
    output  = Stemming(sentence)
    return output

# count term frequency
def Tf(sentence,word):
    tokens =  Tokenizing(sentence)
    for key, value in tokens.iteritems():
        tokens[key] = math.log(1 + value)
    try:
        return tokens[word]
    except KeyError:
        return 0
    

def Idf(number_document,frequency):  
    if frequency == 0 :
        return 0
    invers = float(1 + number_document)/float( 1 + frequency)
    output =  math.log(invers)
    return output

# number of documents containing terms in the corpus
def Frequency(documents,term):
    frequency = 0
    for key, document in documents.iteritems():
        document = Preprocessing(document)
        terms = document.split()
        if term in terms:
            frequency = frequency + 1
    return frequency
    
def TfIdf(article,documents):
    sentence =  Preprocessing(article)
    n_document =  len(documents)
    scores = {}
    for document_id, document_data in documents.iteritems():
        document_data = Preprocessing(document_data)
        document_term = sentence.split()
        for term in document_term:
            frequency_term = Tf(document_data,term)
            frequency  = Frequency(documents,term)
            tf_idf = frequency_term * Idf(n_document,frequency)
            try:
                scores[document_id] = scores[document_id] + tf_idf
            except KeyError:
                if tf_idf > 0:
                    scores[document_id] =  tf_idf
               
    scores = sorted(scores.items(), key=lambda x: x[1],reverse=True)
    return scores

documents  = {}  
documents[1] = "Banyak yang Meragukannya Karena Usia, Ini Kata Mahathir Mohamad" 
documents[2] = "Eksklusif : Wan Azizah: Mahathir dan Anwar Ibrahim Bahas Kabinet"
documents[3] = "Najib Razak Dicekal Usai Kalah di Pemilu Malaysia, Mahathir: Kami Ingin Mengembalikan Aturan Hukum"
documents[4] = "Anwar Ibrahim Akan Bebas pada 15 Mei 2018?"
documents[5] = "Prabowo Subianto: Malu saya dengan Mahathir Mohamad"
documents[6] = "Najib Razak kalah dalam pemilu Malaysia"

article = "Mahathir akan Bebaskan Anwar Ibrahim, Setelah 18 Tahun Bermusuhan"


recomendation = TfIdf(article,documents)
for key,val in recomendation:
    print str(val) + " - " + documents[key]
