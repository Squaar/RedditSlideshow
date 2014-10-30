import praw
import argparse
from urllib.request import urlopen

class RedditSlideshow:

	def __init__(self):
		parser = argparse.ArgumentParser()
		parser.add_argument("file", help="The file containing a list of subreddits, one per line, to read in from.")
		parser.add_argument("number", type=int, default=20, nargs="?", help="The number of submissions to pull from each subreddit")
		parser.add_argument("list", default="hot", nargs="?", help="hot, new, rising, controversial, or top.")
		self.args = parser.parse_args()

		#check if list is valid
		validLists = ["hot", "new", "rising", "controversial", "top"]
		self.args.list = self.args.list.lower()
		if self.args.list not in validLists:
			print("List is not valid. redditslideshow.py -h for help.")
			exit()

		self.reddit = praw.Reddit(user_agent="RedditGrabber v0.1")
		self.subs = self.get_sub_names()
		self.urls = self.get_submission_urls()
		self.clean_urls()

	def get_sub_names(self):
		subs = []
		with open(self.args.file, 'r') as subsFile:
			for line in subsFile:
				line = line.strip()
				if len(line) > 0:
					subs.append({"name": line, "sub": self.reddit.get_subreddit(line)})
		return subs


	def run(self):
		for i, url in enumerate(self.urls):
			print(url + '... ', end='')
			with open(url.split('/')[-1].split('?')[0], 'wb') as f:
				try:
					f.write(urlopen(self.urls[i]).read())
					print('SUCCESS')
				except Exception as e:
					print('FAIL')
					print(e)
		self.cleanup()

	def cleanup(self):
		pass

	#grabs submissions from subreddits and returns list of urls
	def get_submission_urls(self):
		urls = []
		for sub in self.subs:
			sub["submissions"] = []
			if self.args.list == "hot":
				for submission in sub["sub"].get_hot(limit=self.args.number):
					sub["submissions"].append(submission)
					if submission.url is not None:
						urls.append(submission.url)

			elif self.args.list == "new":
				for submission in sub["sub"].get_new(limit=self.args.number):
					sub["submissions"].append(submission)
					if submission.url is not None:
						urls.append(submission.url)

			elif self.args.list == "rising":
				for submission in sub["sub"].get_rising(limit=self.args.number):
					sub["submissions"].append(submission)
					if submission.url is not None:
						urls.append(submission.url)

			elif self.args.list == "controversial":
				for submission in sub["sub"].get_controversial(limit=self.args.number):
					sub["submissions"].append(submission)
					if submission.url is not None:
						urls.append(submission.url)

			elif self.args.list == "top":
				for submission in sub["sub"].get_top(limit=self.args.number):
					sub["submissions"].append(submission)
					if submission.url is not None:
						urls.append(submission.url)
		return urls

	#tries to remove non images, and add file extensions to dumb imgur posts
	def clean_urls(self):
		for url in self.urls:
			if "imgur.com" in url and url[-4] != ".":
				self.urls.remove(url)
				url = url + ".png"
				self.urls.append(url)
			elif ".htm" in url or url[-1] == "/" or "reddit.com" in url or url[-4] != ".":
				self.urls.remove(url)
				continue

if __name__ == '__main__':
	RedditSlideshow().run()





