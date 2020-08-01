from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import pandas as pd
import numpy as np
import re
from nltk.tokenize import TweetTokenizer
import jieba
import hanzidentifier
import random
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

# read in files into dataframes
print("Making dataframes...")
weibo_url = "https://raw.github.ubc.ca/MDS-CL-2019-20/Social_Media_Corpus_on_COVID-19/master/Corpus/data/final_corpus_Weibo_with_annotation.csv?token=AAAAOLTCF7IV3AHNIJLNVE26QDU3Q"
twitter_url = "https://raw.github.ubc.ca/MDS-CL-2019-20/Social_Media_Corpus_on_COVID-19/master/Corpus/data/final_corpus_twitter_with_annotation.csv?token=AAAAOLQBPTSSRYFTEI7NQU26QDU5C"
weibo_df = pd.read_csv(weibo_url, index_col=0)
twitter_df = pd.read_csv(twitter_url, index_col=0)
weibo_annotated_df = weibo_df[weibo_df.annotations.notnull()]
twitter_annotated_df =  twitter_df[twitter_df.annotation.notnull()]
weibo_mask_url = "https://raw.github.ubc.ca/MDS-CL-2019-20/Social_Media_Corpus_on_COVID-19/master/Image/weibo_mask.jpg?token=AAAAOLTJUMVW2YJ7WN62B4S6QDXTW"
twitter_mask_url = "https://raw.github.ubc.ca/MDS-CL-2019-20/Social_Media_Corpus_on_COVID-19/master/Image/twitter_mask.png?token=AAAAOLWQHK7EP32ZT2CWS2S6QDXVU"
cn_stopwords_url = "https://raw.github.ubc.ca/MDS-CL-2019-20/Social_Media_Corpus_on_COVID-19/master/file/cn_stopwords.txt?token=AAAAOLXLPOG2NMCAXI7DNLC6QDU7O"


lemmatizer = WordNetLemmatizer()
tweet_tokenizer = TweetTokenizer(strip_handles=True, preserve_case=False)

# create and read in stopwords
cn_stopwords_df = pd.read_csv(cn_stopwords_url, index_col=0, header=None, names=["stopwords"]).reset_index()
chinese_stopwords = set(cn_stopwords_df["stopwords"])
english_stopwords = set(stopwords.words('english'))
delete_set = {'', '#', '全文', '##', '视频'}
chinese_stopwords.update(delete_set)
punc_en = set(['.', ',', ':', '?', '!', '-', '’', '"', '&', '...', ')', '(', "'", '$', '/', '%', '*', '|', '..', '“', '”','️'])
english_stopwords.update(punc_en)


# two functions required for processing corpora
def lemmatize(keyword):
    """
    Returns the lemma of an English word using NLKT's WordNetLemmatizer().

    Argument:
    keyword -- (str) a string of characters to lemmatize.
    """
    lemma = lemmatizer.lemmatize(keyword, 'v')
    if lemma == keyword:
        lemma = lemmatizer.lemmatize(keyword, 'n')
    return lemma


def process_tweets(string):
    """
    Converts the raw tweet by lowering case, lemmatizing and tokenizing with using NLTK's TweetTokenizer. Returns 
    a list of lemmas.

    Argument:
    string -- (str) a string that is the raw tweet.
    """
    processed = []
    tokens = tweet_tokenizer.tokenize(string)
    for token in tokens:
        processed.append(lemmatize(token.lower()))
    return processed


# four functions required for searching posts by keyword or annotation
def get_indices(keyword, dataframe):
    """
    Retrieves document indexes from the dataframe based on the keyword. Returns a list of integers that correspond to the tweet or Weibo post
    index in the corresponding corpus.
    
    Arguments:
    keyword -- (str) a string that is either English or Chinese.
    dataframe -- (pd.DataFrame) a corpus of social media posts from Twitter or Weibo.
    """
    indices = []
    if hanzidentifier.has_chinese(keyword):
        indices.extend(dataframe[dataframe['text'].str.contains(keyword)].index)
    else:
        word_regex = r"[a-z]+"
        match = re.match(word_regex, keyword)
        if match:
            indices.extend(dataframe[dataframe['joined_lems'].str.contains(pat=fr'\b{keyword}\b',
                                                                           regex=True, case=False)].index)
    return indices


def get_posts(keyword, indices_list, dataframe):
    """
    Uses the indices retrieved by get_indices() to return a list of raw posts. Three conditions are required for
    showing the correct message: (1) singular, (2) plural with no click-again-comment, or (3) plural with 
    click-again-comment. A maximum of 10 posts are returned, and if the length of indices exceed 10, posts are 
    randomly selected. Returns a list of strings. 
    
    Arguments:
    keyword -- (str)  a string that is either English or Chinese.
    indices_list -- (list) list of integers corresponding to the index of a dataframe.
    dataframe -- (pd.DataFrame) a corpus of social media posts from Twitter or Weibo.
    """
    if len(indices_list) == 1:
        posts = [
        f'There is {len(indices_list)} post in the corpus with "{keyword}".']
        posts.append(dataframe.loc[dataframe.index == indices_list, "text"].iloc[0])
    elif len(indices_list) <= 10:
        print("keyword", keyword)
        posts = [
        f'There are {len(indices_list)} posts in the corpus with "{keyword}".']
        for post_index in indices_list:
            posts.append(dataframe.loc[dataframe.index == post_index, "text"].iloc[0])
    else:
        posts = [
            f'There are {len(indices_list)} posts in the corpus with "{keyword}". Click submit again to see different samples.']
        random_list = []
        if len(indices_list) > 10:
            random_list.extend(random.sample(range(0, len(indices_list)),
                                            10))  # generate random integers to determine which posts to return
            for rand in random_list:
                posts.append(dataframe.loc[dataframe.index == indices_list[rand], "text"].iloc[0])
    return posts

def create_wc(word, indices_list, filename, dataframe):
    """
    Generate and return a word cloud based on the keyword.

    Arguments:
    word -- (str) a string that is either English or Chinese.
    indices_list -- (list) list of integers corresponding to the index of a dataframe.
    filename -- (str)
    dataframe -- (pd.DataFrame) a corpus of social media posts from Twitter or Weibo.
    """
    all_posts = []
    response_weibo = requests.get(weibo_mask_url)
    response_twitter = requests.get(twitter_mask_url)
    background_cn = np.array(Image.open(BytesIO(response_weibo.content)))
    background_en = np.array(Image.open(BytesIO(response_twitter.content)))

    if hanzidentifier.has_chinese(word):
        font_path = 'SourceHanSansSC-Regular.otf' #need to download the font file before loading
        background = background_cn
        stopwords = chinese_stopwords
    else:
        font_path = None
        background = background_en
        stopwords = english_stopwords

    for post_index in indices_list:
        all_posts.append(dataframe.loc[dataframe.index == post_index, "text"].iloc[0])

    wordcloud = WordCloud(background_color='white',
                            max_words=100,
                            width=200, height=100,
                            font_path='SourceHanSansSC-Regular.otf',
                            mask=background,
                            stopwords=stopwords).generate(" ".join(all_posts))

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.figure(figsize=(1000, 500))
    wordcloud.to_file(filename)

def dropdown_menu(category, lang):
    """
    Returns a list of raw posts based on the annotation category and language. 

    Arguments:
    category -- (str) the annotation category.
    lang -- (str) the language that posts should be in. 
    """
    list_of_posts = []
    if lang == 'en':
        sd = twitter_annotated_df[
            (twitter_annotated_df.annotation == category) & (twitter_annotated_df.language == lang)]
        list_of_posts = sd['text'].to_numpy()

    if lang == 'cn':
        sd = weibo_annotated_df[(weibo_annotated_df.annotations == category) & (weibo_annotated_df.language == lang)]
        list_of_posts = sd['text'].to_numpy()
    #print(list_of_tweets[:1])
    
    if len(list_of_posts) < 10:
        len_text = f'There are {len(list_of_posts)} posts in the annotation "{category}".'
        new_list = np.insert(list_of_posts, 0, len_text)
        return new_list
    else:
        random.shuffle(list_of_posts)
        len_text = f'There are {len(list_of_posts)} posts in the annotation "{category}". Click submit again to see different samples.'
        new_list = np.insert(list_of_posts, 0, len_text)
        return new_list[:11]


# two functions required for putting returned posts into tables
def create_row(items):
    """
    Converts a list of returned posts into a format compatible for html rows in a html table. Returns a string.

    Arguments: 
    items -- (list) a list of strings that are raw tweets or Weibo posts.
    """
    S = []
    for item in items:
        S.append("<tr>")
        S.append("<td>" + item + "</td>")  
        S.append("</tr>")
    return "".join(S)


def put_in_table(posts):
    """"
    Converts the output from create_row() into a format that is an html table. Returns a string.

    Argument:
    posts - (list)  a list of strings that are raw tweets or Weibo posts.
    """
    return "<table border='1' cellpadding='5' cellspacing='5' width = '800'>" + create_row(posts) + "</table>"



# process df to suit search functions: 1)tokenize twitter with TweetTokenizer, lower and lemmatize tweets,
# 2)tokenize weibo with jieba
twitter_df["tokenized_text"] = twitter_df["text"].map(lambda x: process_tweets(x))  # tokenize, lower and lemmatize
twitter_df["joined_lems"] = twitter_df["tokenized_text"].map(
    lambda x: " ".join(x))  # use for searching quickly searching lemma in text
weibo_df["tokenized_text"] = weibo_df["text"].map(lambda x: list(jieba.cut(x, cut_all=True)))

print("Building vocabularies...")
chinese_vocab = np.unique(np.hstack(weibo_df.tokenized_text)).tolist()
english_vocab = np.unique(np.hstack(twitter_df.tokenized_text)).tolist()

print("Ready for query...")

class MyWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        query = parse.urlsplit(self.path).query  
        query_dict = parse.parse_qs(query)
        if "keyword_search_frontend.css" in self.path:
            self.send_header('Content-type', 'text/css; charset=utf-8')
            self.end_headers()
            f = open("keyword_search_frontend.css", encoding="utf-8")
            html = f.read()
            f.close()
            self.wfile.write(html.encode("utf-8"))
        elif "keyword_search_frontend.js" in self.path:
            self.send_header('Content-type', 'text/javascript; charset=utf-8')
            self.end_headers()
            f = open("keyword_search_frontend.js", encoding="utf-8")
            html = f.read()
            f.close()
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/":
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            f = open("keyword_search_frontend.html", encoding="utf-8")
            html = f.read()
            f.close()
            self.wfile.write(html.encode("utf-8"))
        elif "png" in self.path:
            self.send_header('Content-type', 'image/png;')
            self.end_headers()
            wc = open("word_cloud.png", "rb")
            self.wfile.write(wc.read())
            wc.close()

        else:

            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            print(query_dict)
            if query_dict['type'][0] == 'category':
                language = query_dict["lang"][0]
                selected_category = query_dict["categories"][0]
                print(language, selected_category)
                results = dropdown_menu(selected_category, language)
                posts_table = put_in_table(results)
                self.wfile.write(b"<html>" + posts_table.encode("utf-8") + b"</html>")
            else:
                keyword = query_dict["keyword"][0]
                if hanzidentifier.has_chinese(keyword): #checks for language
                    dataframe = weibo_df
                else:
                    keyword = lemmatize(keyword.lower())
                    dataframe = twitter_df

                if keyword in english_vocab or keyword in chinese_vocab: #checks if keyword in corpus
                    doc_indices = get_indices(keyword, dataframe)
                    results = get_posts(keyword, doc_indices, dataframe)
                    create_wc(keyword, doc_indices, "word_cloud.png", dataframe)
                    posts_table = put_in_table(results)
                    random_num = str(random.randint(1, 1000))
                    self.wfile.write(b"<html>" + posts_table.encode("utf-8") + b'<img src="word_cloud.png?' + random_num.encode("utf-8") + b'">' + b"</html>" )
                else:
                    message = f'Sorry, "{keyword}" is not in our corpus. Make sure the keyword is only one word and there are no spaces.'
                    self.wfile.write(b"<html>" + message.encode("utf-8") + b"</html>")


if __name__ == "__main__":
    http_port = 9999
    server = HTTPServer(('localhost', http_port), MyWebServer)
    server.serve_forever()

