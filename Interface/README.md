# Interface Description

The web interface consists of: 

1. the static component which introduces our corpus.
2. the dynamic component which accesses our corpus. 

The css file divides these components so that (1) is displayed on the majority of the screen to the right, while (2) is on the left side and occupying a small portion of the screen. The css file ensures that returned results from the dynamic component does not jump to a new webpage, which results in a smoother user experience. 

#### (1) The static component - the homepage:

All the content in this component are generated by using static html tags in the html code.

**a. Graphics: word clouds and bar graphs**

The webpage first displays two word cloud images in Chinese and English, generated directly from our corpus and inserted as images in the code. This gives users a quick sense of the corpus because the size of the words corresponds to the frequency of their occurrence in the corpus.  

![](https://raw.githubusercontent.com/moolieloo/Social_media_corpus_on_COVID_19/master/Image/wc_en.png)

There are also two bar graphs on the homepage that illustrate the breakdown of our annotated corpus.

![](https://raw.githubusercontent.com/moolieloo/Social_media_corpus_on_COVID_19/master/Image/barchart.png)

**b. Text:**

Following the word clouds are a brief description of the corpus and annotations, as well as corpus statistics for both sources, Twitter and Weibo. Additional links to the [Annotation Guidelines](https://github.com/moolieloo/Social_media_corpus_on_COVID_19/blob/master/Corpus/Annotation_Guidelines.md) and [Corpus README](https://github.com/moolieloo/Social_media_corpus_on_COVID_19/blob/master/Corpus/README.md) are provided in case users want to learn more.

![](https://raw.githubusercontent.com/moolieloo/Social_media_corpus_on_COVID_19/master/Image/corpus_desc2.png)

#### (2). The dynamic component - search functions:

There are two options -- search by keyword or by a combination of language and annotation -- that enable users to dynamically access the corpus and see social media posts based on their query. All the content in this component are generated by the following workflow: 

1. a query is sent from an html form element.
2. javascript connects the query from html to the python file with the `submit_form()` function. Since we have two queries inside one form, arguments in `submit_form()` determine which query should be sent to python to process. 
3. python carries out the query, performs the approproriate function based on the query and returns the results to html to display. Technically, the python code prebuilds the corpus before any query and stores the data in dataframes. Any query can quickly access the dataframes to return the right information. When a word cloud is returned, the image object is generated by using the package `WordCloud`, saved on users' hard disk and is called again to be rendered in html by using </img> tag. The same file is overwritten for each word cloud creation.

**a. Search by keyword**:

The `text-box` allows users to input free text, either in English or Chinese, into the search box. A sample of 10 posts or less are displayed, depending on how many posts contain the keyword. If more than 10 posts are found in the results, users can can click the `Submit` button again to see different posts. A corresponding word cloud is also generated. This component accesses the entire corpus.

![](https://raw.githubusercontent.com/moolieloo/Social_media_corpus_on_COVID_19/master/Image/keyword_demo.png)

**b. Search by categories and language:**

This component contains two input items. Users can select any of the annotation categories with a `drop-down` menu, and then choose a language with a `radio button`. After receiving the query, the webpage displays a message summarizing the total number of posts found and a sample of 10 posts. User can click the `Submit` button again to see a different sample of posts. This component accesses the annotated part of the corpus.

![](https://raw.githubusercontent.com/moolieloo/Social_media_corpus_on_COVID_19/master/Image/dropdown_demo.png)
