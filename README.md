Information Tracer API Python library
----------------------------

### Who we are
- [Information Tracer](https://informationtracer.com) is a system to trace and summarize information across multiple social media platforms. We current cover 5 platforms -- Twitter, Facebook, Reddit, Youtube and Gab. We are adding Telegram and Instagram.
- This repo provides a Python interface to trace any URL / keyword / hashtag via our API.
- To learn more about system design please check [our paper](http://ceur-ws.org/Vol-2890/paper3.pdf) 

__Due to API limit, each trace call will take 1-3 minutes depending on data volume.__




### pre-requisite 
- python 2 or 3
- you must already have a token

### installation

```bash
pip install informationtracer
```


### usage
```python
from informationtracer import informationtracer
informationtracer.trace(keyword='exposefauci.com', token=YOUR_TOKEN, output_dir='output_test')

```

Parameters

- `keyword`: can be a string (`"BLM"`) or a list of strings (`["BLM", "GunControl", "exposefauci.com"]`)
- `output_dir`: directory under which data will be saved. For each job, a json file name with name `job_id.json` will be created. For example: `/User/test/`
- `output_filename`: the exact path which the data will be saved. For example: `/User/test/result.json` (if you specify `output_filename`, it will overwrite `output_dir`)


### result
```
import json
result = json.load(open('LOCAL_JSON_FILE', 'r'))
```


The payload looks something like this
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
    "term": "Dimejibankole",
    "topics": [
        "election",
        "politics"
    ]
}
```


### behaviors we currently track
| Behavior | Description |
| --- | --- |
| multiple_platform_spread | URL/Keyword is shared on 3 or more platforms, each platform having at least 100 impressions |
| twitter_amplification | average tweet per user is more than 2, or percent of tweets from top 10 percent users is more than 30 |
| youtube_amplification | total number of youtube videos is more than 10 |


### media coverage
[Information Tracer, a proactive framework to fight COVID-19 infodemic](https://nyudatascience.medium.com/cds-guest-editorial-information-tracer-a-proactive-framework-to-fight-covid-19-infodemic-3f9766936f94)
[NYC Media Lab Announces Inaugural Cohort of AI & Local News Challenge](https://www.nycmedialab.org/ai-local-news-blog-update/nyc-media-lab-announces-inaugural-cohort-of-ai-amp-local-news-challenge) 


Author: Zhouhan Chen
Contact: zhouhan.chen@nyu.edu


