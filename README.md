# Social_Media_Corpus_on_COVID-19

Welcome to our bilingual social media corpus collected from Twitter and Weibo in March 2020. English tweets and Chinese Weibo posts related to COVID-19 are the focus of this corpus.


### Setting up the web interface

Please follow these instructions in order to use our web interface.

**Downloads**

The following files need to be downloaded from the repository and saved to the same directory:

1. `keyword_search_backend.py`: the backend python code.
2. `keyword_search_frontend.css`: the style sheets for displaying the html in a certain way.
3. `keyword_search_frontend.html`: the html code that displays is used by the browser to render the html tags.
4. `keyword_search_frontend.js`: the java script code to join the html to the backend Python code.
5. `SourceHanSansSC-Regular.otf`: dependent file for generating word clouds.

It is important to save them all in the same `../user_dir` directory!

![](https://github.ubc.ca/MDS-CL-2019-20/Social_Media_Corpus_on_COVID-19/blob/master/Image/make_dirs_demo.png)

**Dependent packages**

Some dependent packages should already be installed on your computer (e.g., nltk, pandas, numpy, random, io, and http). Please ensure the following packages are also installed:

- jieba: `pip install jieba`
- hanzidentifier: `pip install hanzidentifier`
- wordcloud: `pip install wordcloud`
- matplotlib: `pip install matplotlib`
- PIL: `pip install Pillow`
- requests: `pip install requests`

### Executing the code

Navigate to the `../user_dir` directory in terminal or command-line interface and run the code `python keyword_search_backend.py`. Wait until you see "Ready for query" as shown; this means the web interface is ready to load in the browser!

![](https://raw.github.ubc.ca/MDS-CL-2019-20/Social_Media_Corpus_on_COVID-19/master/Image/execute_demo.png)

Now, open a browser in your system (preferably Chrome) and paste `localhost:9999` in the address bar. You will be able to see the webpage like below:
 
![](https://raw.github.ubc.ca/MDS-CL-2019-20/Social_Media_Corpus_on_COVID-19/master/Image/webpage_demo.png)

<u>Troubleshooting</u>

If you encounter a problem with the port, try changing the port number `9999` in line 308 of `keyword_search_backend.py` to any unused port in your local system.

### How to use the web interface:

**Search by keyword**

- Enter the keyword in English or Chinese in the `text box` and press the `Submit` button to see a list of returned posts and a word cloud that matches the query.

![](https://raw.github.ubc.ca/MDS-CL-2019-20/Social_Media_Corpus_on_COVID-19/master/Image/keyword_demo.png)

<u>Please note: </u>

- Keywords must be one word with no spaces. For example, a search for "virus\ " will not return any posts. However, if the input is "virus", a total of 3,052 posts will be found and a random sample of 10 from the search results will be displayed. One Chinese word can be multiple characters. The same no-space rule applies; a search like "学校" (meaning school) will return 59 posts but "学\ 校" will not.
- Do not press the `enter` key because the query will not send. Click `Submit` only.
- There may be some lag after submitting the keyword due to the word cloud generation, please be patient.
- To see different social media posts if more than 10 were found, click the `Submit` button again.

<u>Suggested searches: </u>

- Try "asldkjb". You will be notified this keyword is not in our corpus.
- Try "test", "testing" and "TeStEd". The returned results are the same because raw data was tokenized, lemmatized and lower-cased.
- Try "what're", "wat" and "what". Different messages will be displayed according to the length of the returned results. 
- Try an emoji... however, nothing will be returned because, sadly, the word cloud package does not handle emojis. 
- Try "李" (a surname) and "李文亮" (the full name of the late Wuhan doctor). Jieba is built for text segmentation and not named entity recognition. Even though "李文亮" is quite common in our corpus, technically it is not in our dictionary. A customized vocabulary dictionary needs to be created and then merged with the existing Jieba dictionary in order to capture names like "李文亮". 
- Try "学校" (simplified Chinese for school) and "學校" (traditional Chinese). And then try "学" (simplified Chinese for to learn) and "學" (traditional Chinese). The Chinese data was not normalized for form so results varied. The vocabulary is built on Jieba's text segmentation of the raw post.

**Search by annoation**

- First, select the annotation category to query in the `drop-down` menu. Then, select the language and click `Submit` to see social media posts that matches the query. If more than 10 posts were found, click the `Submit` button again to see a different batch of posts.

![](https://raw.github.ubc.ca/MDS-CL-2019-20/Social_Media_Corpus_on_COVID-19/master/Image/dropdown_demo.png)

<u>Please note: </u>

- Do not press the `enter` key because the query will not send. Click `Submit` only.



