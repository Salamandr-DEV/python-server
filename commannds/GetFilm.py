import gridfs
import requests
import urllib.parse
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import json


def Get_Film(self, name, db):
    self.send_response(200)
    info = main(name)
    #fileName = "https://osiris.load.hdrezka-ag.net/movies/2557c285fbe0c4d44f7b6f9820204839e4b763ef/bdf78129edda021dbdf079638afda23c:2020071011/1080.mp4"
    self.send_header('Content-type', "text/plain")
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()
    self.wfile.write(bytes(info, "utf8"))

def Get_Info_Film(self, name, db):
    self.send_response(200)
    info = main(name)
    self.send_header('Content-type', "text/plain")
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()
    self.wfile.write(bytes(info, "utf8"))

class MyHTMLParser(HTMLParser):

    # def handle_starttag(self, tag, attrs):
    #     print("Encountered a start tag:", tag)
    #
    # def handle_endtag(self, tag):
    #     print("Encountered an end tag :", tag)

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        check_ultra = data.find('Ultra')
        check_1080 = data.find('[1080p]')
        check_720 = data.find('[720p]')
        check_480 = data.find('[480p]')
        new_url = ""
        if check_ultra != -1:
            beg = data.find("Ultra")
            end = data.find(":hls", beg)
            if beg != "":
                url = data[beg + 6 : end]
                for i in url:
                    if i == "\\":
                        new_url += ""
                    else:
                        new_url += i
            return new_url
        elif check_1080 != -1:
            beg = data.find("1080")
            end = data.find(":hls", beg)
            if beg != "":
                url = data[beg + 6 : end]
                for n in url:
                    if n == "\\":
                        new_url += ""
                    else:
                        new_url += n
            return new_url
        elif check_720 != -1:
            beg = data.find("720")
            end = data.find(":hls", beg)
            if beg != "":
                url = data[beg + 6 : end]
                for j in url:
                    if j == "\\":
                        new_url += ""
                    else:
                        new_url += j
            return new_url

def parse_searching_films(filename):
    results = []
    text = filename

    soup = BeautifulSoup(text, 'lxml')
    film_list = film_list = soup.find('div', {'class': 'b-content__inline_items'})
    items = film_list.find_all('div', {'class': 'b-content__inline_item'})
    for item in items:
        movie_link = item.find('div', {'class': 'b-content__inline_item-link'}).find('a').get('href')
        movie_desc = item.find('div', {'class': 'b-content__inline_item-link'}).find('a').text
        movie_info = item.find('div', {'class': 'b-content__inline_item-link'}).find('div').text

        results.append({
                'movie_link': movie_link,
                'movie_name': movie_desc,
                'movie_info': movie_info
            })
    return results

def parse_info_film(filename):
    results = dict(info=[])
    text = filename

    soup = BeautifulSoup(text, 'lxml')

    film_list = film_list = soup.find('div', {'class': 'b-content__main'})
    info = film_list.find_all('div', {'class': 'b-post__infotable clearfix'})
    info_text = film_list.find_all('div', {'class': 'b-post__description'})

    movie_title = film_list.find('div', {'class': 'b-post__title'}).text
    try:
        movie_origin_title = film_list.find('div', {'class': 'b-post__origtitle'}).text
    except:
        movie_origin_title = ''

    try:
        movie_image = info[0].find('div', {'class': 'b-post__infotable_left'}).find('div',
                                                                                    {'class': 'b-sidecover'}).find(
            'a').get('href')
    except:
        movie_image = ''

    try:
        movie_post_info = info[0].find('div', {'class': 'b-post__infotable_right'}).find('div',
                                                                                         {
                                                                                             'class': 'b-post__infotable_right_inner'}).find(
            'table', {'class': 'b-post__info'}).find_all('tr')
    except:
        movie_post_info = ''

    try:
        movie_info_text = info_text[0].find('div', {'class': 'b-post__description_text'}).text
    except:
        movie_info_text = ''

    results['info'].append({
        'movie_title': movie_title,
        'movie_origin_title': movie_origin_title,
        'movie_image': movie_image,
        'movie_info_text': movie_info_text
    })

    for data in movie_post_info:
        movie_data_2 = data.find_all('td')
        for data_2 in movie_data_2:
            movie_data = data_2.text
            results['info'].append({
                'movie_data': movie_data,
            })

    return results

def check(title):
    name = ""
    for symb in title:
        if symb == "/":
            name += " "
        elif symb == ":":
            name += " "
        elif symb == "*":
            name += " "
        elif symb == "?":
            name += " "
        elif symb == "+":
            name += " "
        elif symb == ";":
            name += " "
        elif symb == "(":
            name += " "
        elif symb == ")":
            name += " "
        else:
            name += symb
    return name

def main(films):
    #film = input()  # "https://osiris.load.hdrezka-ag.net/movies/8fc1119009cc84a4a07d8e56bf675d094beb9425/772dfc0b9fa3f0c32884d3e85875d431:2020030823/1080.mp4"

    # encode_film = urllib.parse.quote(film)
    #
    # response = requests.get("https://rezka.ag/index.php?do=search&subaction=search&q=" + encode_film)
    # res = response.text
    # #print(res)
    #
    # films = parse_searching_films(res)
    #
    # response = requests.get(films[0]["movie_link"])
    # res = response.text

    response = requests.get(films)
    res = response.text

    Film = parse_info_film(res)

    # url_image = str(Film[0]['movie_image'])
    # image = requests.get(url_image)
    #
    # title_film = check(films[0]['movie_name'])

    # f = open(title_film + ".jpg", "wb")
    # f.write(image.content)
    # f.close()

    parser = MyHTMLParser()
    url = parser.handle_data(res)
    Film['info'].append({
                'movie_link': url,
            })

    json_string = json.dumps(Film)

    return json_string

