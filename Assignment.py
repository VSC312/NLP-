#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import re
from collections import Counter


# In[4]:


#Downloading NLTK components
nltk.download('punkt')
nltk.download('stopwords')


# In[5]:


# Read input Excel file
input_df = pd.read_excel(r"C:\Users\vardhan\Downloads\Input.xlsx")


# In[6]:


#Function to scrape text from articles
def scrape_article(url, article_tags=None):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize an empty list to store article text
        article_text_list = []
        
        # Iterate over the specified HTML elements (tags)
        if article_tags:
            for tag in article_tags:
                elements = soup.find_all(tag)
                for element in elements:
                    article_text_list.append(element.get_text())
        
        # If no specific tags are specified, we will assume <p> tags
        if not article_text_list:
            article_text_list = [p.get_text() for p in soup.find_all('p')]
        
        # Combine the text from all identified elements
        article_text = ' '.join(article_text_list)
        
        return article_text
    except requests.RequestException:
        return None


# In[7]:


pip install pyphen


# In[8]:


pip install nltk


# In[9]:


from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import pyphen
#Implementing steps as provided in the text analysis document
# Downloading NLTK resources 
nltk.download('punkt')
nltk.download('stopwords')

def analyze_text(text, pos_words, neg_words, stop_words):
    # Step 1: Cleaning using Stop Words Lists
    stop_words = set(stopwords.words('english'))
    
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    # Remove stopwords and punctuation from words
    cleaned_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    
    # Step 2: Creating a dictionary of Positive and Negative words (unchanged)
    positive_words = set()
    negative_words = set()
    
    with open(r'C:\Users\vardhan\Downloads\MasterDictionary-20240126T075608Z-001\MasterDictionary\positive-words.txt', 'r') as pos_file:
        positive_words = set(pos_file.read().split())
    
    with open(r'C:\Users\vardhan\Downloads\MasterDictionary-20240126T075608Z-001\MasterDictionary\negative-words.txt', 'r') as neg_file:
        negative_words = set(neg_file.read().split())
    
    # Step 3: Extracting Derived variables
    positive_score = sum(1 for word in cleaned_words if word in positive_words)
    negative_score = sum(1 for word in cleaned_words if word in negative_words)
    
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 0.000001)
    
    # Step 4: Analysis of Readability (unchanged)
    total_words = len(cleaned_words)
    total_sentences = len(sentences)
    avg_sentence_length = total_words / total_sentences
    
    complex_words = [word for word in cleaned_words if len(word) > 2]  # Complex words have more than 2 characters
    percentage_complex_words = len(complex_words) / total_words
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    avg_words_per_sentence = total_words / total_sentences
    
    complex_word_count = len(complex_words)
    
    # Step 5: Word Count (already obtained as total_words)
    
    # Step 6: Syllable Count Per Word
    dic = pyphen.Pyphen(lang='en')
    syllable_counts = [len(dic.inserted(word).split('-')) for word in cleaned_words]
    
    # Step 7: Personal Pronouns (unchanged)
    personal_pronoun_count = len(re.findall(r'\b(I|we|my|ours|us)\b', text, flags=re.IGNORECASE))
    
    # Step 8: Average Word Length (unchanged)
    total_characters = sum(len(word) for word in cleaned_words)
    avg_word_length = total_characters / total_words
    
    # Return analysis results as a dictionary
    analysis_results = {
        "PositiveScore": positive_score,
        "NegativeScore": negative_score,
        "PolarityScore": polarity_score,
        "SubjectivityScore": subjectivity_score,
        "AvgSentenceLength": avg_sentence_length,
        "PercentageComplexWords": percentage_complex_words,
        "FogIndex": fog_index,
        "AvgWordsPerSentence": avg_words_per_sentence,
        "ComplexWordCount": complex_word_count,
        "WordCount": total_words,
        "SyllableCountPerWord": syllable_counts,
        "PersonalPronounCount": personal_pronoun_count,
        "AvgWordLength": avg_word_length
    }
    
    return analysis_results


# In[10]:


# Load stop words and sentiment words
stop_words = set(stopwords.words('english'))
additional_stop_files = [
    r'C:\Users\vardhan\Downloads\StopWords-20240126T075017Z-001\StopWords\StopWords_Auditor.txt',
    r'C:\Users\vardhan\Downloads\StopWords-20240126T075017Z-001\StopWords\StopWords_DatesandNumbers.txt',
    r'C:\Users\vardhan\Downloads\StopWords-20240126T075017Z-001\StopWords\StopWords_Generic.txt',
    r'C:\Users\vardhan\Downloads\StopWords-20240126T075017Z-001\StopWords\StopWords_GenericLong.txt',
    r'C:\Users\vardhan\Downloads\StopWords-20240126T075017Z-001\StopWords\StopWords_Geographic.txt',
    r'C:\Users\vardhan\Downloads\StopWords-20240126T075017Z-001\StopWords\StopWords_Names.txt',
    r'C:\Users\vardhan\Downloads\StopWords-20240126T075017Z-001\StopWords\StopWords_Currencies.txt'  # New stop words file
]

for file_path in additional_stop_files:
    with open(file_path, 'r') as file:
        stop_words.update(file.read().split())

with open(r'C:\Users\vardhan\Downloads\MasterDictionary-20240126T075608Z-001\MasterDictionary\positive-words.txt', 'r') as file:
    pos_words = set(file.read().split())
with open(r'C:\Users\vardhan\Downloads\MasterDictionary-20240126T075608Z-001\MasterDictionary\negative-words.txt', 'r') as file:
    neg_words = set(file.read().split())


# In[ ]:


# Iterating over the input DataFrame
for index, row in input_df.iterrows():
    article_text = scrape_article(row['URL'])
    if article_text:
        analysis_results = analyze_text(article_text, pos_words, neg_words, stop_words)


# In[ ]:


# Create an empty list to store analysis results for all articles
all_analysis_results = []

# Iterating over the input DataFrame
for index, row in input_df.iterrows():
    article_text = scrape_article(row['URL'])
    
    if article_text:
        try:
            analysis_results = analyze_text(article_text, pos_words, neg_words, stop_words)
            all_analysis_results.append(analysis_results)
        except Exception as e:
            # Handle exceptions (e.g., log the error)
            print(f"Error analyzing article {index}: {str(e)}")

# Now all_analysis_results contains the results for all articles
# You can save or further process this data as needed


# In[ ]:




