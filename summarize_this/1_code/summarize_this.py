# Step 1: Preparing the data

import nltk
import bs4 as BeautifulSoup
import urllib.request
import sys  
from nltk.tokenize import word_tokenize, sent_tokenize


# Fetching the content from the URL
fetched_data = urllib.request.urlopen(sys.argv[1])


article_read = fetched_data.read()

# Parsing the URL content and storing in a variable
article_parsed = BeautifulSoup.BeautifulSoup(article_read,'html.parser')

# Returning <p> tags
paragraphs = article_parsed.find_all('p')

article_content = ''

# Looping through the paragraphs and adding them to the variable
for p in paragraphs:  
    article_content += p.text


# Step 2: Processing the data
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
def _create_dictionary_table(text_string) -> dict:
   
    # Removing stop words
    stop_words = set(stopwords.words("english"))
    
    words = word_tokenize(text_string)
    
    # Reducing words to their root form
    stem = PorterStemmer()
    
    # Creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table

_create_dictionary_table(article_content)

from nltk.tokenize import word_tokenize, sent_tokenize


sentences = sent_tokenize(article_content)

# Step 4: Finding the weighted frequencies of the sentences

def _calculate_sentence_scores(sentences, frequency_table) -> dict:   

    # Algorithm for scoring a sentence by its words
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]

        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] /        sentence_wordcount_without_stop_words
      
    return sentence_weight

# because _calculate_sentence_scores takes a frequency table as an input
# we need to define a frequency table here:
frequency_table_of_article_content = _create_dictionary_table(article_content)


# now let's input our frequency table along with our sentences

# this is how we're evaluating the score for every sentence in the text.
# we've analyzed the frequency of occurence of each term. 
# In this case, we’ll be scoring each sentence by its words; that is, adding the frequency of each important word found in the sentence.
_calculate_sentence_scores(sentences, frequency_table_of_article_content)




# Step 5: Calculating the threshold of the sentences

def _calculate_average_score(sentence_weight) -> int:
   
    # Calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # Getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score

# create a variable that is the calculated sentence weight
sentence_weight_calculated = _calculate_sentence_scores(sentences, frequency_table_of_article_content)  


# now perform this function on that in order to calculate the average score

threshold_of_sentences = _calculate_average_score(sentence_weight_calculated)


# Step 6: Getting the Summary

def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary

# This output is now a summary of a wikipedia page!

article_summary = _get_article_summary(sentences, sentence_weight_calculated, threshold_of_sentences)

# print out the article summary
print(article_summary)

# save the article summary as a txt file
# with open(sys.argv[1].split('/', -1)[-1] + '.txt', "w") as text_file:
#     text_file.write(article_summary)


