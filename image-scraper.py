import praw
import urllib.request
import os
import sys

iterations = 1
if len(sys.argv) == 2 and sys.argv[1] == "--all":
	iterations = 10

reddit = praw.Reddit(client_id="", client_secret="-c", password="", user_agent="image-scraper by /u/NIPE-SYSTEMS", username="")
params = {}
for i in range(iterations):
	for post in reddit.subreddit("MostBeautiful").new(params=params):
		try:
			print("Download {} -> {}".format(post.url, "imgs/{}".format(post.name)), end="")
			if os.path.exists("imgs/{}".format(post.name)):
				print(" already existing")
				continue
			if post.score < 100:
				print(" score too low")
				continue
			if post.preview["images"][0]["source"]["width"] < 1920 or post.preview["images"][0]["source"]["height"] < 1080:
				print(" dimensions too low")
				continue
			print(" ...")
			urllib.request.urlretrieve(post.url, "imgs/{}".format(post.name))
		except AttributeError: # sometimes post.preview isn't available
			pass
		params["after"] = post.name
