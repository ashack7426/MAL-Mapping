from lxml import html
import requests
import json
import time
import io
import bs4 as BeautifulSoup4
import re

# profile
# anime days vs Rating
# manga days vs rating
# Theory is more you watch the rating will go down ?
# Also I think after a certain point you just start reading more manga


# Manga graph
# Thickness of lines represents shared users (weight)
# If 2 peeps share an anime in common then they have a line
# Find the anime clusters

# Anime graph
# Same thing as manga graph


# Just do 2 graphs


def get_top_anime():
    link = 'https://myanimelist.net/topanime.php?type=bypopularity'
    page = requests.get(link)
    tree = html.fromstring(page.content)
    lst = tree.xpath(
        '//h3[@class="hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3"]/a/text()')

    cnt = 50
    while cnt < 1100:
        new_link = link + "&limit=" + str(cnt)
        page = requests.get(new_link)
        tree = html.fromstring(page.content)
        lst += tree.xpath(
            '//h3[@class="hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3"]/a/text()')
        cnt += 50

    return lst


def get_top_manga():
    link = 'https://myanimelist.net/topmanga.php?type=bypopularity'
    page = requests.get(link)
    tree = html.fromstring(page.content)
    lst = tree.xpath('//h3[@class="manga_h3"]/a/text()')

    cnt = 50
    while cnt < 1100:
        new_link = link + "&limit=" + str(cnt)
        page = requests.get(new_link)
        tree = html.fromstring(page.content)
        lst += tree.xpath('//h3[@class="manga_h3"]/a/text()')
        cnt += 50
    return lst


def get_users():
    link = 'https://myanimelist.net/users.php?lucky=1'
    page = requests.get(link)
    tree = html.fromstring(page.content)
    names = tree.xpath('//td[@align="center"]/div/a/text()')
    return names

# Completed or plan to watch


def get_anime(user, top):
    lst = []

    for i in [1, 2, 6]:
        link = 'https://myanimelist.net/animelist/' + \
            user + "?status=" + str(i)
        page = requests.get(link)
        tree = html.fromstring(page.content)

        try:
            anime = tree.xpath('//table[@class="list-table"]/@data-items')[0]
            anime.replace("[", "{")
            anime.replace("]", "}")
            anime = json.loads(anime)

            for ani in anime:
                name = str(ani["anime_title"])
                if name in top:
                    lst.append(name)
        except:
            pass

    return lst

# Completed or plan to watch


def get_manga(user, top):
    lst = []

    for i in [1, 2, 6]:
        link = 'https://myanimelist.net/mangalist/' + \
            user + "?status=" + str(i)
        page = requests.get(link)
        tree = html.fromstring(page.content)

        try:
            manga = tree.xpath('//table[@class="list-table"]/@data-items')[0]
            manga.replace("[", "{")
            manga.replace("]", "}")
            manga = json.loads(manga)

            for mag in manga:
                name = str(mag["manga_title"])
                if name in top:
                    lst.append(name)
        except:
            pass

    return lst


def get_profile(user):
    link = 'https://myanimelist.net/profile/' + user
    page = requests.get(link)
    tree = html.fromstring(page.content)
    scores = []
    days = tree.xpath('//div[@class="di-tc al pl8 fs12 fw-b"]/text()')

    # Anime score
    for i in range(11):
        txt = '//div[@class="stats anime"]//span[@class="score-label score-' + \
            str(i) + '\"]/text()'
        score = tree.xpath(txt)

        if score:
            scores.append(score[0])

    # Manga score
    for i in range(11):
        txt = '//div[@class="stats manga"]//span[@class="score-label score-' + \
            str(i) + '\"]/text()'
        score = tree.xpath(txt)

        if score:
            scores.append(score[0])

    # days, mean
    if not days:
        days = ['0', '0']
    if not scores:
        scores = ['0', '0']

    if days == ['0', '0'] and scores == ['0', '0']:
        time.sleep(20)

    profile = [days, scores]
    return profile


def write_edges(lst, path):
    for name1 in lst.keys():
        for name2 in lst.keys():
            if name1 != name2:
                cnt = 0
                for user in lst[name1]:
                    if user in lst[name2]:
                        cnt += 1

                if cnt:
                    txt = name1 + "," + name2 + "," + str(cnt) + "\n"
                    path.write(txt)
