Corpus + explanation
================

#### Overview

Our **[corpus](https://github.ubc.ca/ltian05/proj_adv_corpus_linguistics/tree/master/corpus)** 
(click here for the collected corpus) comprises of two csv files, one for each source, 
[Weibo](https://www.weibo.com/us) and
[Twitter](https://twitter.com). We searched for posts that referenced
the coronavirus. The available, scrapable, data from each source
differed slightly, so the information we scrapped for each source are
also different.

#### Twitter

We collected Twitter data in three separate runs, according to our
targeted regions by using the search term “\#coronavirus”. The files
were concatenated into one final csv file in post-processing. The
following information is stored in the corpus:

  - tweet id - unique identifier for each tweet.
  - tweet content - the full text that was tweeted.
  - language - “en”; we limited the search to English.
  - created at - the time and date that the tweet was posted.
  - month - the month of that the tweet was posted; extracted from the
    original created\_at date.
  - day - the day of the month; extracted from the original created\_at
    date.
  - source - “twitter”; since there are two sources in this corpus, we
    thought it may be helpful to track the source of the data.
  - region: one of “north america”, “europe”, or “india”; we used the
    following geolocations to establish where the post originated:
      - North America = “41.2565,-95.9345,2500km” \#geolocation for
        Omaha
      - Europe = “52.52,13.4050,1500km” \#geolocation for Berlin
      - India = “20.5937,78.9629” \#geolocation for Maharashtra
  - corpus statistics:
      - number of tweets: 48,656
      - number of words: 1,343,207
      - average length of tweets: 28 words

**Known problems**

  - Duplicates - although our code filtered out retweets and only
    captured tweets with unique ids, there are still some instances of
    duplicates. Tweets where content is copy-and-pasted are scraped. We
    removed duplicates in post-processing.
  - Historical data limitations - since Twitter only allows data to be
    downloaded in the past 7 days, a significant amount of tweets
    reference similar content or event. Our original plan of conducting
    a diachronic analysis of tweets using our corpus is probably not
    possible.
  - Noise - the data includes hashtags, mentions (referring to a
    particular person) and various url links. This will not affect the
    annotation process.

#### Weibo

We collected Weibo data in twelve separate runs, according to different
keyword searches. The files were concatenated into one final csv file in
post-processing. The following information was collected and stored as a
csv file after each search:

  - post content - up to a maximum of about 150 Chinese characters.
    Please see “Known problems” below for more details.
  - language - “cn”. Please see “Known problems” below for more details.
  - created at - the time and date of the post
  - month - the month of the post; extracted from the original
    created\_at date.
  - day - the day of the month; extracted from the original created\_at
    date.
  - source - “weibo”
  - region: “China”; we may choose to remove this metadata. Please see
    “Known problems” below for more details.
  - corpus statistics:
      - number of posts: 4,566
      - number of characters: 528,954
      - average length of post: 155 characters

**Known problems**

  - Duplicates - we are scraping from Weibo’s search results webpages
    and this method did not filter out duplicates. We removed duplicates
    in post-processing.
  - Truncated post content - posts from Weibo’s search results limits
    the display of the post to a maximum length of about 150 Chinese
    characters. We were only able to scrap what was displayed. This does
    not appear to be a big issue as the annotation can be successfully
    completed without seeing the full text.  
  - Language - while most posts are in Chinese, some are a mixture of
    English and Chinese. On a few rare occassions where users posted in
    English only, we removed those in post-processing.
  - Region - we were unable to accurately track the location of the
    posts because this information was simply unavailable. Our input of
    “China” is an assumption we made knowing the overwhelming majority
    of Weibo users are Chinese. However, we are also aware that users
    may not be posting from China. We may remove this column from the
    csv file altogether.
  - Noise - the data includes hashtags, mentions (referring to a
    particular person) and various url links. This will not affect the
    annotation process.
  - Data limitations - Weibo returns a limited of number webpages when
    we use its search function to find posts related to the coronavirus.
    The number of returned webpages depends on the keyword, since some
    keywords are more referenced than others. We managed to iterate
    through 100 webpages for some popular keywords. There are about 8-10
    posts per returned webpage. The Weibo scraping method we implemented
    limited our ability to collect data for the corpus. We (somewhat)
    overcame this obstacle by using different keywords to obtain more
    posts. However, our corpus is still highly imbalanced considering we
    scraped 48,656 tweets and only 4,566 Weibo posts. Given more time,
    we would find and use more efficient ways to scrap Weibo. However,
    we did the best we could under the circumstances. The keywords we
    used are:
      - COVID\_19
      - 医生 - doctor
      - 口罩 - facemasks
      - 封城 - lockdown
      - 新冠 - novel\_coronavirus pneumonia
      - 李文亮 - name of famous doctor
      - 武汉肺炎 - wuhan\_coronavirus (ran search twice)
      - 疫情 - epidemic
      - 肺炎超话 - coronavirus\_supertopic
      - 隔离 - quarantine (ran search twice)
