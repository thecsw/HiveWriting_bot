"""
This is the main u/HiveWriting_bot script that posts new
submissions and then waits for a day. After the waiting is
over, check for the top comments and test them against our
sentence regex. The first one passes will be used as next
sentence.
"""
import time
import re
from datetime import date
import praw
import config

def main():
    # Initialize the reddit instance
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         username=config.USERNAME,
                         password=config.PASSWORD,
                         user_agent=config.USER_AGENT)

    # Fill the initial poem text
    plot_text = ""
    with open('poem.txt', 'r'):
        plot_text = r.readlines()

    # The regex sentence matching and extracting pattern
    pattern = r'^\s*([A-Za-z0-9,;\'\"\s]{1,128}[.?!])\s*$'
    prog = re.compile(pattern)

    # Specify the subreddit where to post
    sub = reddit.subreddit('HiveWriting')

    # Start posting submissions and pinning them
    while True:
        # Post the submission
        post = sub.submit(f'Sentence for {date.today().timetuple()[1]}/{date.today().timetuple()[2]}/{date.today().timetuple()[0]}!',
                          selftext='The current plot:\n' + plot_text,
                          flair_text='TBD')

        # Sticky the post to the subreddit
        post.mod.approve()
        post.mod.distinguish()
        post.mod.sticky()

        # Wait for 24 hours
        time.sleep(24 * 60 * 60)

        # Start parsing the top top-level only comments
        post.comments.comment_sort = 'top'
        post.comments.replace_more(limit=0)
        found = False
        for comment in post.comments:
            reg_m = prog.match(comment.body)
            if reg_m is not None:
                plot_text += reg_m.group(0)
                found = True
                break

        # What if no good sentence found?
        if not found:
            post.mod.flair(text='SENTENCE NOT FOUND')
        else:
            post.mod.flair(text='SENTENCE FOUND')

        # Unsticky the post
        post.mod.sticky(state=False)

        # Write the text to the file just in case
        with open('poem.txt', 'w') as w:
            w.write(plot_text)

        # And then the whole loop repeats itself

if __name__ == '__main__':
    main()
