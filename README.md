Information Tracer API Python library
----------------------------

### Who we are
- Information Tracer provides cross-platform social media intelligence about how information (URL, keyword, hashtag) spreads online. We implement an ensemble of metrics to indicate suspicious spread patterns. 
- We currently cover 5 platforms -- Twitter, Facebook, Reddit, Youtube and Instagran.
- Below is a diagram of our system design. To learn more please check [our paper](http://ceur-ws.org/Vol-2890/paper3.pdf) 

![Information Tracer architecture](./img/information-tracer-pipeline.png)

__Due to API limit, each trace call will take 1-3 minutes depending on data volume.__

### Pre-requisite 
- python 3
- you must already have a token

### installation

```bash
pip install informationtracer
```


### usage
```python
from informationtracer import informationtracer
id_hash256 = informationtracer.trace(query='free crypto', token=YOUR_TOKEN)

```

Parameters
- `query`: a string of one or multiple words. For example: `"GunControl", "free crypto", "EritreaOutOfTigray"
- `token`: contact us to get your token

Return Value (__please save and keep a record for future use__)
- `id_hash256`: a unique identifier for each query.  How to use `id_hash256`?
  - Visualize results by visiting https://informationtracer.com/?result={id_hash256}  (need to log in first)
  - Get results from result API endpoint https://informationtracer.com/api/v1/result?token={token}&id_hash256={id_hash256}


### result 
- The result is automatically saved in a local json file `result_{id_hash256}.json`. If you set `--skip_result`, no result will be saved
- If you set `--result_filename /User/abc/Downloads/result.json`, result will be saved at your designated location

result format
```
{
    "behaviors": ["multiple_platform_spread"],
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
        "original_tweet": [],
        "original_tweet_detail": [],
        "reddit": [],
        "reply": [
            {
                "d": "@haidaer__ \ud83e\udd14",
                "i": 0,
                "n": "ebikhay",
                "t": "2022-05-14T08:48:16"
            },
        ],
        "retweet": [
            {
                "d": "RT @Emiee___: #NewProfilePic Happy Sunday and Mother\u2019s Day to all the mothers out there, it\u2019s been a while, I should get more active here\ud83e\udd14\u2026",
                "i": 1,
                "n": "theswiish",
                "t": "2022-05-08T14:12:12"
            },
        ],
        "telegram": [],
        "youtube": []
    },
    "id_hash256": "a21c353de8b231a458b88db0ee8f483ccd2b38482d82f3556b443b2071cec819",
    "topics": [
        "election",
        "politics"
    ]
}
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



