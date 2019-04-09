import praw
import config

def main():
    # Initialize the reddit instance
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         username=config.USERNAME,
                         password=config.PASSWORD,
                         user_agent=config.USER_AGENT)
    print("Started.")
    for submission in reddit.redditor('HiveWriting_bot').submissions.top('all'):
        submission.mod.remove()
    print("Done.")

if __name__ == '__main__':
    main()
