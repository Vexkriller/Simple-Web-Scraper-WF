import json
import praw
import requests
from bs4 import BeautifulSoup

result = requests.get("https://worldflipper.playkakaogames.com")
soup = BeautifulSoup(result.text,"html.parser")
urls = []
urls2= []
urls3= []

def poster(newlink):

	temptitles = []
	result2 = requests.get(newlink)
	soup2 = BeautifulSoup(result2.text,"html.parser")

	for h2_tag in soup2.find_all("div"):
		a_tag = h2_tag.find('h2')
		if a_tag == None:
			continue
		else:
			temptitles.append(a_tag)

	title = ((str(temptitles[2])).replace('</h2>','')).replace('<h2 class="tit_news">','')

	credentials = 'client_secrets.json' 
	with open(credentials) as f:
    		creds = json.load(f)
			
	reddit = praw.Reddit(client_id=creds['client_id'],
                     	client_secret=creds['client_secret'],
                     	user_agent=creds['user_agent'],
                     	redirect_uri=creds['redirect_uri'],
                     	refresh_token=creds['refresh_token'])

	subreddit = reddit.subreddit("worldflipper") 

	subreddit.submit(title,url = newlink,flair_id = "763f2db2-f8de-11eb-86b9-52a387d657fd")

for h2_tag in soup.find_all("li"):
	a_tag = h2_tag.find("a")
	if a_tag == None:
		continue
	else:
		if "/news/" in a_tag.attrs['href']:
			urls.append(a_tag.attrs['href'])
			urls3.append(a_tag.attrs['href'])

textfile = open("wf.txt", "r")
readline = textfile.readlines()

urls2.append(readline[0].strip())
urls2.append(readline[1].strip())
urls2.append(readline[2].strip())

n = 3

if urls2[0] in urls:
	urls3.remove(urls2[0])
	n -= 1

if urls2[1] in urls:
	urls3.remove(urls2[1])
	n -= 1

if urls2[2] in urls:
	urls3.remove(urls2[2])
	n -= 1

if n == 0:
	exit()

else:
	for i in range(n):
		newlink = "https://worldflipper.playkakaogames.com" + urls[i]
		poster(newlink)

textfile = open("wf.txt", "w")
for element in urls:
    textfile.write(element + "\n")
textfile.close()

exit()