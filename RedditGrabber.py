import praw
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", help="The file containing a list of subreddits, one per line, to read in from.")
parser.add_argument("list", default="hot", nargs="?", help="hot, new, rising, cotroversial, or top.")
args = parser.parse_args()

reddit = praw.Reddit(user_agent="RedditGrabber v0.1")

subsFile = open(args.file, "r")
subs = []
for line in subsFile:
	line = line.strip()
	if len(line) > 0:
		subs.append({"name": line, "sub": reddit.get_subreddit(line)})
subsFile.close()

#print(str(subs))

for submission in subs[0]["sub"].get_hot(limit=10):
	print(submission.short_link)
	print(submission.url)
	print()