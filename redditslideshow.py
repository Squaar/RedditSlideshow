import praw
import argparse
from urllib.request import urlopen

#grabs submissions from subreddits and returns list of urls
def getSubmissions(sub, number, list):
	urls = []
	for sub in subs:
		sub["submissions"] = []

		if list == "hot":
			for submission in sub["sub"].get_hot(limit=args.number):
				sub["submissions"].append(submission)
				if submission.url is not None:
					urls.append(submission.url)

		elif list == "new":
			for submission in sub["sub"].get_new(limit=args.number):
				sub["submissions"].append(submission)
				if submission.url is not None:
					urls.append(submission.url)

		elif list == "rising":
			for submission in sub["sub"].get_rising(limit=args.number):
				sub["submissions"].append(submission)
				if submission.url is not None:
					urls.append(submission.url)

		elif list == "controversial":
			for submission in sub["sub"].get_controversial(limit=args.number):
				sub["submissions"].append(submission)
				if submission.url is not None:
					urls.append(submission.url)

		elif list == "top":
			for submission in sub["sub"].get_top(limit=args.number):
				sub["submissions"].append(submission)
				if submission.url is not None:
					urls.append(submission.url)
	return urls

#tries to remove non images, and add file extensions to dumb imgur posts
def cleanURLs(urls):
	for url in urls:
		if "imgur.com" in url and url[-4] != ".":
			urls.remove(url)
			url = url + ".png"
			urls.append(url)
		elif ".htm" in url or url[-1] == "/" or "reddit.com" in url or url[-4] != ".":
			urls.remove(url)
			continue
		



parser = argparse.ArgumentParser()
parser.add_argument("file", help="The file containing a list of subreddits, one per line, to read in from.")
parser.add_argument("number", type=int, default=20, nargs="?", help="The number of submissions to pull from each subreddit")
parser.add_argument("list", default="hot", nargs="?", help="hot, new, rising, controversial, or top.")
args = parser.parse_args()

#check if list is valid
validLists = ["hot", "new", "rising", "controversial", "top"]
args.list = args.list.lower()
if args.list not in validLists:
	print("List is not valid. redditslideshow.py -h for help.")
	exit()

reddit = praw.Reddit(user_agent="RedditGrabber v0.1")

#set up list of subreddits
subsFile = open(args.file, "r")
subs = []
for line in subsFile:
	line = line.strip()
	if len(line) > 0:
		subs.append({"name": line, "sub": reddit.get_subreddit(line)})
subsFile.close()

urls = getSubmissions(subs, args.number, args.list)
cleanURLs(urls)

# for url in urls:
# 	print(url)

for i in range(0,len(urls)):
	f = None
	try:
		f = open(str(i) + ".png", "wb")
		f.write(urlopen(urls[i]).read())
		f.close()
		print(str(i) + ".png downloaded!")
	except:
		f.close()
		print(str(i) + ".png failed!")

print("done.")