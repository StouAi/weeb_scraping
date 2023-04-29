import requests
from bs4 import BeautifulSoup as bs

def info(manga, check_tags=None):
    #finding the info we want to print and checking for errors
    try:
        author = manga.find('span', class_='text-nowrap item-author').text
    except AttributeError:
        author = 'unknown'
    manga_title = manga.find('h3', {'class': 'item-title'}).text
    try:
        latest_chapt = manga.p.a['href']
    except AttributeError:
        latest_chapt = 'no chapters yet'

    if check_tags == []:
        print(f'{manga_title.strip()}')
        print(f'written by {author}')
        print(f'latest chapter link: {latest_chapt}\n')
    elif check_tags == None:
        print(f'{manga_title.strip()}')
        print(f'written by {author}')
        print(f'latest chapter link: {latest_chapt}\n')
    else:
        return
if __name__=="__main__":
    #gets url of main page
    html_text = requests.get('https://manganato.com/').text
    #we use soup to turn html to desired format and then we find use find
    soup = bs(html_text,'lxml')
    mangas = soup.find_all('div', class_='content-homepage-item')
    print("Manga updates:")
    #get user input as a list
    user_genres=input("Enter the tags you want to be included seperated by comma(,) or simply press Enter\n").split(',')
    f_user_tags=[user_tag.capitalize() for user_tag in user_genres ]

    for manga in mangas:
        #iterating the mangas list
        #case that user didnt input tags so we can skip the search for them
        if f_user_tags[0]!='':
            #enter the page for the manga
            looktag= requests.get(manga.a['href']).text
            tagsoup=bs(looktag,'lxml')
            #find the genre tags
            tagger=tagsoup.find('div',class_='story-info-right')
            tagged=tagger.find_all('a',class_='a-h')
            genre =tagged[1:]
            genre_text=[tag.text for tag in genre]
            #if user_genre are not in the manga add them to check_genre
            check_genre=[tag for tag in f_user_tags if tag not in genre_text]
            info(manga, check_genre)
        else:
            info(manga)
