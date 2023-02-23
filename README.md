Information Tracer API Python library
----------------------------

### Who we are
- [Information Tracer](https://informationtracer.com) provides cross-platform social media intelligence about how information (URL, keyword, hashtag) spreads online. 
- Some features: search any keyword during any time period; get top posts per platform; visualize sharing network; access indicators of suspicious behaviors. 
- We currently cover 5 platforms -- Twitter, Facebook, Reddit, Youtube and Instagram.
- Below is a diagram of our system design. To learn more please check [our paper](http://ceur-ws.org/Vol-2890/paper3.pdf) 

![Information Tracer architecture](./img/information-tracer-pipeline.png)

__Due to API limit, each trace call will take 30-60 seconds depending on data volume.__

### Pre-requisite 
- python 3
- you must already have a token

### installation

```bash
pip install informationtracer
```


### Trace API (send query and get results)
```python
from informationtracer import informationtracer
id_hash256 = informationtracer.trace(query='free crypto', token=YOUR_TOKEN)
```

Parameters
- `query`: [REQUIRED] a string of one or multiple words. For example: "GunControl", "free crypto". We support boolean operators like AND, OR, NOT. See [How to build a complex query](#how-to-build-a-complex-query) to learn more.
- `token`: [REQUIRED] contact us to get your token
- `start_date`: all posts are published after this date, format YYYY-MM-DD, default 7 days before current date
- `end_date`: all posts are published before this date, format YYYY-MM-DD, default current date
- `label`: label for this query. Default is "API_submit"
- `skip_result`: By default, the result is automatically saved to a local json file `result_{id_hash256}.json`. If you add `skip_result=True`, no json will be saved
- `result_filename`: Default is None. If you add `result_filename="/User/abc/Downloads/result.json"`, result will be saved at your designated location.

Return Value (__please save and keep a record for future use__)
- `id_hash256`: a unique identifier for each query.  How to use `id_hash256`?
  - Visualize results by visiting https://informationtracer.com/?result={id_hash256}  (need to log in first)
  - Retrieve results later from result API (see below)

### Result API (get results. must have sent the query before)
```python
import requests
url = "https://informationtracer.com/api/v1/result?token={}&id_hash256={}".format(YOUR_TOKEN, id_hash256)
results = requests.get("url").json()
```

### How to build a complex query
#### Important rules
- `AND`, `OR`, `NOT` must be all-cap. Otherwise they are treated as normal English words
- Use parenthesis to group multiple words with AND. For example, `(Word1 AND Word2)`
- Query limit is 512 characters. Sending a query above the limit might get empty results.

Example: `(Ukraine AND NATO) OR (Ukraine AND EU)`
Meaning: Any posts that contain "Ukraine" and "NATO" or "Ukraine" and "EU".

Example: `(Ukraine AND NATO) NOT Biden NOT Putin`
Meaning: Any posts that contain "Ukraine" and "NATO", without word "Biden" or "Putin".

### Format of result 
by default, result is a json with multiple fields

- `query`: the search query 
- `id_hash256`: unique ID for this query
- `posts`: social media posts on each platform. Each post has four parameters:
 - `d`: (description, basically the text)
 - `i`: (number of interaction)
 - `n`: (name of the account/group/channel)
 - `t`: (time of the post)
- `metrics`: summary of the information spread  
- `indicators`: suspicious behaviors we track
- `co_occurrence`: list of urls and hashtags that appear together with the query
- `created_at`: query collection time

```
{
    "query": "Sample query"
    "metrics": {
        "avg_tweet_per_user": 1.2072072072072073,
        "breakout_scale": 3,
        "top_10_percent_tweet": 0.24253731343283583,
        "total_interaction": 2968
    },
    "posts": {
        "facebook": [
            {
                "d": "None",
                "i": 99,
                "n": "Objectv Media",
                "t": "2021-01-16T07:16:31"
            },
            {
                "d": "None",
                "i": 33,
                "n": "Who to Vote Nigeria",
                "t": "2021-03-12T21:05:02"
            },
        ],
        "reddit": [],
        "twitter": [
            {
                "d": "@haidaer__ \ud83e\udd14",
                "i": 0,
                "n": "ebikhay",
                "t": "2022-05-14T08:48:16"
            },
        ],        
        "youtube": []
    },
    "co_occurrence": [
        {
          "count": 54,
          "name": "POPULAR_URL",
          "platform": "facebook",
          "type": "url"
        },
        {
          "count": 44,
          "name": "SAMPLE_HASHTAG",
          "platform": "twitter",
          "type": "hashtag"
        },
        {
          "count": 36,
          "name": "SAMPLE_HASHTAG_2",
          "platform": "facebook",
          "type": "hashtag"
        }
    ],
    "indicator": {
        "contains_sensitive_topic": {
          "context": null,
          "verdict": false
        },
        "coordinated_across_platforms": {
          "context": null,
          "verdict": false
        },
        "has_twitter_bot_activity": {
          "context": null,
          "verdict": false
        },
        "overall_information_quality": 100,
        "shared_by_suspicious_account": {
          "context": null,
          "verdict": false
        },
      },    
    "id_hash256": "a21c353de8b231a458b88db0ee8f483ccd2b38482d82f3556b443b2071cec819",
    "created_at": "Mon, 23 Jan 2023 12:26:55 GMT",
}
```

### Load Source API (get detailed posts from individual platform)
```python
import requests
url = "https://informationtracer.com/loadsource?source={}&id_hash256={}&token={}".format(SOURCE, id_hash256, YOUR_TOKEN)
results = requests.get("url").json()
```





### Web interace 
- To help people visualize the information, we provide a web interface available at [https://informationtracer.com](https://informationtracer.com). 
- To visualize a query you searched recently, you can visit `https://informationtracer.com/?result={id_hash256}`. 

![Screenshot of Information Tracer Wen Interface](./img/information-tracer-web-interface-screenshot.png)



### Media coverage
- [Information Tracer, a proactive framework to fight COVID-19 infodemic](https://nyudatascience.medium.com/cds-guest-editorial-information-tracer-a-proactive-framework-to-fight-covid-19-infodemic-3f9766936f94)
- [NYC Media Lab Announces Inaugural Cohort of AI & Local News Challenge](https://www.nycmedialab.org/ai-local-news-blog-update/nyc-media-lab-announces-inaugural-cohort-of-ai-amp-local-news-challenge) 


### Contact / Bug Report
For bug report or any inquiry, please contact Zhouhan Chen zhouhan.chen@nyu.edu



