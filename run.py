import requests
from bs4 import BeautifulSoup
from winotify import Notification, audio
import time




# setup the url
URL = "https://www.tinnitustalk.com/find-new/posts"

# create a Post class
class Post:
    def __init__(self, title, link, author, date, replies, views):
        self.title = title
        self.link = link
        self.author = author
        self.date = date
        self.replies = replies
        self.views = views

    def __repr__(self):
        return f"{self.title} by {self.author} on {self.date}"

    def __eq__(self, other):
        return self.title == other.title and self.author == other.author and self.date == other.date

# create a list of posts
post_list = []
new_post_list = []


# loop every minute
while True:
    # print the time
    print(time.strftime("%H:%M:%S", time.localtime()))

    # get the page
    # catch any errors
    try:
        headers = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
        page = requests.get(URL, headers=headers)
    except:
        print("Error")
        # sleep for 5 minutes
        time.sleep(300)
        continue
    
    # parse the page
    soup = BeautifulSoup(page.content, "html.parser")

    # get the main content of the page
    results = soup.find(id="content")

    # find all the posts
    posts = results.find_all("li", class_="discussionListItem visible")

    # loop through the posts
    for post in posts:
        title_element = post.find("h3", class_="title")
        title = title_element.text.strip()
        author_element = post.find("div", class_="listBlock lastPost")
        # author = author_element.text.strip()
        author = author_element.find("a", class_="username").text.strip()
        link = None
        date = author_element.find("a", class_="dateTime").text.strip()
        replies = None
        views = None

        new_post_list.append(Post(title, link, author, date, replies, views))
        # print(title, author, date)

    # check if the post list has changed
    first_run = post_list == []
    post_list_changed = post_list != new_post_list

    # a variable to store the new posts
    new_posts = []
    if any([first_run, post_list_changed]):
        print("changed")
        # print only the new posts updates:
        post_num = 0
        for post in new_post_list:
            if post not in post_list:
                post_num += 1
                print(f"{post_num:2}. {post}")
                new_posts.append(post)

        # for index, post in enumerate(new_post_list, start=1):
        #     print(f"{index:2}. {post}")
        print()

        # set message containing the new posts' titles in new line
        message = "\n".join([post.title for post in new_posts])

        # setup the notification
        toast = Notification(app_id="TinnitusTalk scraper",
                                title=f"{len(new_posts)} new posts",
                                msg=message,
                                duration="long",
                                icon=r"C:\nir\scraper\tinnitustalk-logo-white.png")

        # setup the audio
        toast.set_audio(audio.Default, loop=False)

        # show the notification
        toast.show()

    # set the post list to the new post list
    post_list = new_post_list

    # clear the new post list
    new_post_list = []

    # sleep for 5 minutes
    time.sleep(300)

# end of script

     