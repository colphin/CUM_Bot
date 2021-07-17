import subprocess
import json
import datetime
import shutil
import requests
import random
import asyncpraw
from decouple import config

class RedditRelay:

    def __init__(self):
        client_id = config('REDDIT_CLIENT_ID')
        secret = config('REDDIT_SECRET')
        self.client = asyncpraw.Reddit(client_id=client_id,
                                  client_secret =  secret,
                                  user_agent = 'CUM/0.0.1')
        
        self.client.close()


    async def closeConnection(self):
        await self.client.close()

    async def getMeme(self, topic = ''):
        # result = requests.get('https://oauth.reddit.com/api/v1/me', headers=self.headers)
        if not topic:
            topicList = [
                "MemeEconomy",
                "ComedyCemetery",
                "dankmemes",
                "memes"
            ]
            random_index = random.randint(0,len(topicList)-1)

            topic = topicList[random_index]

        subreddit = await self.client.subreddit(topic, fetch=True)
        meme = await subreddit.random()
        try:
            _ = meme.preview
            result = {
                    "code":200,
                    "subreddit": topic,
                    "title": meme.title,
                    "url": meme.url,
                    "ups": meme.ups,
                    "author": meme.author.name,
                    "spoilers_enabled": subreddit.spoilers_enabled,
                    "nsfw": subreddit.over18,
                    "image_previews": [i["url"] for i in meme.preview.get("images")[0].get("resolutions")]
                }
        except Exception as e:
            result = {
                    "post_link": meme.shortlink,
                    "subreddit": topic,
                    "title": meme.title,
                    "url": meme.url,
                    "ups": meme.ups,
                    "author": meme.author.name,
                    "spoilers_enabled": subreddit.spoilers_enabled,
                    "nsfw": subreddit.over18,
                    "image_previews": ["No Preview Found For This Meme.. Sorry For That"]
                }
        
        return result
        

        

