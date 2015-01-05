
#-*- coding: utf-8 -*-
import time
import requests
import BeautifulSoup
import transmissionrpc

url = 'http://www.togoons.com/bbs/board.php?bo_table=torrent_variety'
host = 'http://www.togoons.com/'
search_keyword = u'김병만의'

def post_torrent(magnet):
  tc = transmissionrpc.Client('localhost', port=9091)
  tc.add_torrent(magnet)

def get_torrent(post_url):
  response = requests.get(post_url)
  soup = BeautifulSoup.BeautifulSoup(response.text)
  elements = soup.findAll('td', attrs={'bgcolor': '#FFFFFF'})
  for element in elements:
    if 'magnet:?xt' in element.text:
      print element.text
      post_torrent(element.text)
      break

def get_posts():
  response = requests.get(url)
  soup = BeautifulSoup.BeautifulSoup(response.text)

  elements = soup.find('table', attrs={'class': 'board_list'}).findAll('tr')
  for element in elements:
    element_class = element.get('class')
    if not (element_class == 'bg0' or element_class == 'bg1'):
      continue

    a_element = element.find('a')

    ret = a_element.text.find(search_keyword, 0, len(a_element.text))
    print ret
    if ret == -1:
      continue
  
    get_torrent(host + a_element['href'][2:])

def main():
  while True:
    get_posts()
    time.sleep(60)

if __name__ == '__main__':
  main()
