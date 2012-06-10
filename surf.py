'''
Created on Jun 9, 2012

@author: akittredge
'''
import urllib2
import BeautifulSoup
import sys
import re
import datetime


def ms_soup(ms_page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'}
    req = urllib2.Request(url='http://magicseaweed.com/%s' % ms_page, 
                          headers=headers)
    page_soup = BeautifulSoup.BeautifulSoup((urllib2.urlopen(req).read()))
    return page_soup
    
def parse_and_print(page_soup):
    swell_height = page_soup.find('h3', text='Swell').findNext('span').string
    swell_direction = page_soup.find('h3', text='Swell').findNext('img')['alt']
    wind_speed = page_soup.find('h3', text='Wind').findNext('span').string
    
    print 'swell: %s, from: %s, wind: %s' % (swell_height, swell_direction, wind_speed)
    height_factor = 2
    forcast_bars = page_soup.findAll('td', {'class' : 'gph'})
    wave_heights = []
    for forcast_bar in forcast_bars:
        timestamp = re.search('timestamp=(\d+)', forcast_bar['onclick']).group(1)
        time = datetime.datetime.fromtimestamp(float(timestamp))
        wave_height = int(re.search('height: (\d+)px;', forcast_bar.div['style']).group(1))
        wave_heights.append(wave_height / height_factor)
        #print '%s, %s' % (time, wave_height * '*')
    
    graph_height = min(100, max(wave_heights))
    column_width = 3
    for height in reversed(range(graph_height)):
        line = ''
        for wave_height in wave_heights:
            if wave_height >= height:
                line += '*' * column_width
            else:
                line += ' ' * column_width
        print line

def main():
    test_page = 'Matunuck-Surf-Report/377/'
    page_soup = ms_soup(test_page)
    parse_and_print(page_soup)
    
if __name__ == '__main__':
    sys.exit(main())