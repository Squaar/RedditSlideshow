import praw
import argparse

#grabs submissions from subreddits
def getSubmissions(sub, number, list):
	for sub in subs:
		sub["submissions"] = []

		if list == "hot":
			for submission in sub["sub"].get_hot(limit=args.number):
				sub["submissions"].append(submission)

		elif list == "new":
			for submission in sub["sub"].get_new(limit=args.number):
				sub["submissions"].append(submission)

		elif list == "rising":
			for submission in sub["sub"].get_rising(limit=args.number):
				sub["submissions"].append(submission)

		elif list == "controversial":
			for submission in sub["sub"].get_controversial(limit=args.number):
				sub["submissions"].append(submission)

		elif list == "top":
			for submission in sub["sub"].get_top(limit=args.number):
				sub["submissions"].append(submission)

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

getSubmissions(subs, args.number, args.list)


for sub in subs:
	print(sub["name"] + ":")
	for submission in sub["submissions"]:
		print("\t" + submission.short_link)
	print()


