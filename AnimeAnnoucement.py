from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import os.path

"""Get the episode from the website using a Get request"""
def getEpisodes(anime):
    url = 'https://animeheaven.ru/detail/' + anime + '-TV'
    uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        webpage = urlopen(uClient).read()
    except HTTPError as err:
        if err.code == 404:
            url = 'https://animeheaven.ru/detail/'+anime
            uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(uClient).read()
        else:
            return -1, -1, -1

    webpage = webpage.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    part = soup.find('div', class_='infopicbox')
    link = part.find('img')['src']
    part2 = soup.find('div', class_='infoepbox')
    episodeList = part2.find_all('a')
    status = soup.find_all('div', class_='infodes2')[1].find_all('div', class_='textc')[-3].getText()
    episodes = []
    for line in episodeList:
        try:
            episode = int(line['title'].split(' ')[-1])
            episodes.append(episode)
        except:
            pass
    return episodes, link, status

def checkStatus(anime):
    url = 'https://animeheaven.ru/detail/' + anime + '-TV'
    uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        webpage = urlopen(uClient).read()
    except HTTPError as err:
        if err.code == 404:
            url = 'https://animeheaven.ru/detail/' + anime
            uClient = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(uClient).read()

    webpage = webpage.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    status = soup.find_all('div', class_='infodes2')[1].find_all('div', class_='textc')
    return status[-3].getText()

"""Check for new anime episode based on logger file"""
def checkNewEpisode():
    # Check if logger file exists
    file_exists = os.path.exists('logger.txt')
    new = False
    newAnimes = []
    if file_exists:
        with open('logger.txt', 'r+') as file:
            data = file.read()
            data = data.split('\n')
            for i in range(0,len(data)-1,2):
                anime = data[i].replace(' ','-')
                newEpisodes, link, status = getEpisodes(anime)
                if newEpisodes == -1:
                    return -1
                if checkStatus(anime) == 'Ongoing':
                    newEpisodes = newEpisodes[::-1]
                    if data[i+1] == '':
                        data[i+1] = newEpisodes
                    else:
                        oldEpisodes = data[i+1].split(',')[:-1]
                        if oldEpisodes[-1] != str(newEpisodes[-1]):
                            data[i+1] = newEpisodes
                            anime = data[i] + ',' + str(newEpisodes[-1]) + ',' + link
                            newAnimes.append(anime)
                            new = True
            rewrite = ''
            i = 0
            while i < len(data)-1:
                eps = ''
                if type(data[i]) == list:
                    for lines in data[i]:
                        eps += str(lines) + ','
                    rewrite += str(eps) + '\n'
                else:
                    rewrite += str(data[i]) + '\n'
                i += 1
            if new == True:
                if type(data[-1]) == list:
                    final = ''
                    for episodes in data[-1]:
                        final += str(episodes) + ','
                    rewrite += final
                else:
                    rewrite += data[-1]
                file.seek(0, 0)
                file.write(rewrite)
                file.close()
                return newAnimes
            else:
                rewrite += data[-1]
                file.seek(0, 0)
                file.write(rewrite)
                file.close()
                return False

"""Check if an anime is in the list"""
def checkList(anime):
    found = False
    file_exists = os.path.exists('logger.txt')
    if file_exists:
        with open('logger.txt', 'r+') as file:
            data = file.read()
            data = data.split('\n')
            for i in range(0, len(data) - 1, 2):
                if data[i].lower() == anime:
                    found = True
            file.close()
        return found


"""Adds anime to the logger"""
def adds(anime):
    #Check if the anime is already in the list or not
    if checkList(anime.lower()) == True:
        return 3, 3, 3
    else:
        #Prepare title name
        name = anime.split(' ')
        title = ''
        for words in name:
            try:
                words = words[0].upper() + words[1:]
                title += words + ' '
            except:
                title += words + ' '
        title = title[:-1]
        name = title.replace(' ', '-')
        episodes, link, status = getEpisodes(name)
        #Check for errors in getting the episodes
        if episodes == -1:
            return -1, -1, -1
        else:
            reversed = episodes[::-1]
            ep = ''
            for episode in reversed:
                ep += str(episode) + ','
            data ='\n' + title + '\n' + ep
            #append to watchlist
            file_exists = os.path.exists('logger.txt')
            if file_exists:
                with open('logger.txt', 'a+') as file:
                    file.write(data)
                    file.close()
            return title, episodes[0], link

"""Returns all the animes and their episodes"""
def listAllBulletin():
    # Check if logger file exists
    file_exists = os.path.exists('logger.txt')
    if file_exists:
        with open('logger.txt', 'r+') as file:
            data = file.read()
            data = data.split('\n')
            rewrite = ''
            i = 0
            while i < len(data)-1:
                eps = ''
                if type(data[i]) == list:
                    for lines in data[i]:
                        eps += str(lines) + ','
                    rewrite += str(eps) + '\n'
                else:
                    rewrite += str(data[i]) + '\n'
                i += 1
            if type(data[-1]) == list:
                final = ''
                for episodes in data[-1]:
                    final += str(episodes) + ','
                rewrite += final
            else:
                rewrite += data[-1]
            file.close()
            return rewrite

"""List the episode of a specific anime"""
def listEpisodes(anime):
    anime = anime.lower()
    if checkList(anime) == False:
        return 2, 2
    file_exists = os.path.exists('logger.txt')
    if file_exists:
        with open('logger.txt', 'r+') as file:
            data = file.read()
            data = data.split('\n')
            for i in range(0,len(data)-1,2):
                if anime == data[i].lower():
                    temp1, link, temp2 = getEpisodes(anime.replace(' ', '-'))
                    return data[i+1], link


"""Remove anime from the logger"""
def removes(anime):
    anime = anime.lower()
    if checkList(anime) == False:
        return 2
    # Check if logger file exists
    file_exists = os.path.exists('logger.txt')
    if file_exists:
        with open('logger.txt', 'r+') as file:
            data = file.read()
            data = data.split('\n')
            for i in range(0, len(data) - 1, 2):
                if data[i].lower() == anime:
                    result = data[:i] + data[i+2:]
            rewrite = ''
            i = 0
            while i < len(result) - 1:
                eps = ''
                if type(result[i]) == list:
                    for lines in result[i]:
                        eps += str(lines) + ','
                    rewrite += str(eps) + '\n'
                else:
                    rewrite += str(result[i]) + '\n'
                i += 1
            rewrite += result[-1]
            file.truncate(0)
            file.seek(0, 0)
            file.write(rewrite)
            file.seek(0,0)
            file.close()
            return 0
