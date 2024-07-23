import requests
import urllib.parse
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import json

def Get_Films(self, name, db):
    self.send_response(200)
    fileName = main(name)
    self.send_header('Content-type', "text/plain")
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()
    self.wfile.write(bytes(fileName, "utf8"))

def Get_page_Films(self, db):
    self.send_response(200)
    fileName = main_page()
    self.send_header('Content-type', "text/plain")
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()
    self.wfile.write(bytes(fileName, "utf8"))


class MyHTMLParser(HTMLParser):

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

def lamb(elem):
    return elem[1]

def parse_searching_films(filename, link):
    results = dict(films=[], pages=[])
    text = filename

    soup = BeautifulSoup(text, 'lxml')
    film_list = soup.find('div', {'class': 'b-content__inline_items'})
    items = film_list.find_all('div', {'class': 'b-content__inline_item'})
    navigation = film_list.find_all('div', {'class': 'b-navigation'})

    for item in items:
        movie_link = item.find('div', {'class': 'b-content__inline_item-link'}).find('a').get('href')
        movie_name = item.find('div', {'class': 'b-content__inline_item-link'}).find('a').text
        movie_info = item.find('div', {'class': 'b-content__inline_item-link'}).find('div').text
        movie_image = item.find('div', {'class': 'b-content__inline_item-cover'}).find('a').find('img').get('src')
        movie_cat = item.find('span', {'class': 'cat'}).find('i').text

        results['films'].append({
                'movie_link': movie_link,
                'movie_name': movie_name,
                'movie_info': movie_info,
                'movie_image': movie_image,
                'movie_cat': movie_cat
            })

    end = link.find('page', 0)
    if end != -1:
        new_link = link[0: end]
        active = link[end+5: -1]
    else:
        new_link = link + "/"
        active = str(1)

    for pages in navigation:
        page = pages.find_all()

        for i in range(0, len(page)-1):
            page_ = page[i].text
            if page_ != "\xa0":
                if page_ != " ":
                    if page_ == "...":
                        page_link = ""
                    else:
                        page_link = new_link + "page/" + page[i].text + "/"
                    if page_ == active:
                        page_class = "active"
                    else:
                        page_class = ""
                    page_name = page[i].text
                    results['pages'].append({
                        'page_link': page_link,
                        'page_name': page_name,
                        'page_class': page_class
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

def main(film):
    encode_film = urllib.parse.quote(film)

    response = requests.get(film)
    res = response.text

    urls_films = parse_searching_films(res, film)

    json_string = json.dumps(urls_films)

    return json_string

def main_page():

    response = requests.get("https://rezka.ag")
    res = response.text

    urls_films = parse_searching_films(res)

    json_string = json.dumps(urls_films)

    return json_string
