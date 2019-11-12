import requests

from bs4 import BeautifulSoup as bs

import sys

from model import ListOrg, Habr, db_session

class ParserListOrg:
    def __init__(self, url: str):
        self.user_agent = {'User-agent': 'Mozilla/5.0'}
        self.url = str(url)

    def get_html(self) -> None:
        self.req = requests.get(self.url, headers=self.user_agent).text

    @staticmethod
    def db_add(firm, args) -> None:
        new_org = ListOrg(firm, args[0], args[1], args[2], args[3], args[4], args[5], args[6])
        try:
            db_session.add(new_org)
            db_session.commit()
        except:
            db_session.rollback()


    def soup_and_info(self) -> None:
        self.get_html()
        soup = bs(self.req, 'lxml')
        c2m = soup.find('div', class_ = 'c2m')
        firm = c2m.find_all('a',class_='upper')[0].text
        trs = c2m.find_all('tr')
        list_with_info = [trs[i].find_all('td') for i in range(len(trs))]
        args = [i[1].text for i in list_with_info]
        self.db_add(firm, args)


class ParserHabr(ParserListOrg):
    def __init__(self, count):
        self.count = count
        self.page = self.count//20
        self.post_count = self.count%20
        self.url = 'https://habr.com/ru/top/yearly/page'
        self._list = []

    def get_html(self) -> None:
        self.req = requests.get(self.url).text

    @staticmethod
    def db_add(nick, date, title, text):
        new_post = Habr(nick, date, title, text)
        try:
            db_session.add(new_post)
            db_session.commit()
        except:
            db_session.rollback()

    def parse_info(self) -> None:
        for el in self._list:
            nickname = el.find('span', class_='user-info__nickname').text
            date = el.find('span', class_='post__time').text
            title = el.find('a', class_='post__title_link').text
            text = el.find('div', class_='post__text').text
            self.db_add(nickname, date, title, text)


    def get_posts(self) -> None:
        url = self.url
        for i in range(1, self.page + 2):
            self.url = url + str(i)
            self.get_html()
            soup = bs(self.req, 'lxml')
            posts = soup.find_all('article', class_='post_preview')[:self.count]
            self.count = self.count - 20
            self._list.extend(posts)
        self.parse_info()





if __name__ == '__main__':
    try:
        habr = ParserHabr(int(sys.argv[1]))
        habr.get_posts()

    except ValueError:
        pars = ParserListOrg(sys.argv[1])
        pars.soup_and_info()
