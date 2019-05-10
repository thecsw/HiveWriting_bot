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
    with open('poem.txt', 'r') as r:
        plot_text = r.read()

    # The interval
    hours = 24
    interval = hours * 3600
    # parts = 24 // hours
    current_part = 0
    current_day = -1

    # The regex sentence matching and extracting pattern
    pattern = r'^\s*([-A-Za-z0-9.,;!?@#$%^&*_(){}+~\'\"\s\n]{1,256}[.?!]?)\s*$'
    prog = re.compile(pattern)

    # Specify the subreddit where to post
    sub = reddit.subreddit('hivewriting')

    # Start posting submissions and pinning them
    while True:
        day = date.today().timetuple()[2]
        month = date.today().timetuple()[1]
        year = date.today().timetuple()[0]

        # Calculate the part
        if current_day == day:
            current_part += 1
        else:
            current_day = day
            current_part = 1

        # Post the submission
        #title = f'Sentence for {month}/{day}/{year}: Part {current_part} of {parts}'
        title = f'Sentence for {month}/{day}/{year}'
        post = sub.submit(title,
                          selftext='The current plot:\n\n' + plot_text)
        print(f"Posted a submission:\n{title}\nWaiting...\n")

        # Sticky the post to the subreddit
        #post.mod.approve()
        post.mod.distinguish()
        post.mod.sticky()

        # Wait for 24 hours
        time.sleep(interval)
        print("Done waiting")
        # Start parsing the top top-level only comments
        post.comments.comment_sort = 'top'
        post.comments.replace_more(limit=0)
        found = False
        for comment in post.comments:
            # Check if the sentence is passing
            reg_m = prog.match(comment.body)
            if reg_m is not None:
                plot_text += reg_m.group(0)
                # If no .?! is found at the end, append a dot by default
                if re.match(r'.+[.?!]$', comment.body) is None:
                    plot_text += '.'
                plot_text += ' '
                found = True
                comment.mod.approve()
                comment.reply('Congrats! Your sentence was chosen! Come check out the new post to continue your story!')
                break

        # What if no good sentence found?
        if not found:
            post.mod.flair(text='SENTENCE NOT FOUND')
        else:
            print('SENTENCE FOUND:\n' + plot_text)
            post.mod.flair(text='SENTENCE FOUND')

        # Unsticky the post
        post.mod.sticky(state=False)
        # Lock the post
        post.mod.lock()

        # Write the text to the file just in case
        with open('poem.txt', 'w') as w:
            w.write(plot_text)

        # And then the whole loop repeats itself

if __name__ == '__main__':
    main()
