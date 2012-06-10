'''
Created on Jun 9, 2012

@author: akittredge
'''
import urllib2
import BeautifulSoup
import sys
import re
import datetime
import struct
import fcntl
import termios


def ms_soup(ms_page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'}
    #req = urllib2.Request(url='http://magicseaweed.com/%s' % ms_page, 
                          #headers=headers)
    #page_soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(req).read())
    page_soup = BeautifulSoup.BeautifulSoup(open('/tmp/mg_seaweed_test_page').read())
    return page_soup

def terminal_width():
    #Return the current width of the terminal.
    #from http://bytes.com/topic/python/answers/607757-getting-terminal-display-size
    try:
        s = struct.pack("HHHH", 0, 0, 0, 0)
        fd_stdout = sys.stdout.fileno()
        x = fcntl.ioctl(fd_stdout, termios.TIOCGWINSZ, s)
        width = struct.unpack("HHHH", x)[1]
    except IOError:
        width = 80
    return width

def parse_and_print(page_soup):
    swell_height = page_soup.find('h3', text='Swell').findNext('span').string
    swell_direction = page_soup.find('h3', text='Swell').findNext('img')['alt'].replace('&deg;', '')
    wind_speed = page_soup.find('h3', text='Wind').findNext('span').string
    wind_direction = page_soup.find('h3', text='Wind').findNext('img')['alt'].replace('&deg;', '')
    
    print 'Swell: %sft, from: %s dgs.' % (swell_height, swell_direction)
    print 'Wind %smph, from %s dgs.' % (wind_speed, wind_direction)
    height_factor = 2
    forcast_bars = page_soup.findAll('td', {'class' : 'gph'})
    wave_heights = []
    time_labels = []
    for forcast_bar in forcast_bars:
        timestamp = re.search('timestamp=(\d+)', forcast_bar['onclick']).group(1)
        time_labels.append(datetime.datetime.fromtimestamp(float(timestamp)).strftime('%H %a'))
        wave_height = int(re.search('height: (\d+)px;', forcast_bar.div['style']).group(1))
        wave_heights.append(wave_height / height_factor)
        
    graph_height = min(100, max(wave_heights))
    column_width = terminal_width() / len(wave_heights)
    for height in reversed(range(graph_height)):
        line = ''
        for wave_height in wave_heights:
            if wave_height >= height:
                line += '*' * column_width
            else:
                line += ' ' * column_width
        print line
    
    time_col = column_width / 2
    time_col_template = (' ' * time_col) + '%s' + (' ' * (column_width - 1 - time_col))

    for time_label_row in range(len(max(time_labels))):
        print ''.join(time_col_template % time_label[time_label_row] for 
                      time_label in time_labels)
        
        
def main():
    test_page = 'Matunuck-Surf-Report/377/'
    page_soup = ms_soup(test_page)
    parse_and_print(page_soup)
    
if __name__ == '__main__':
    sys.exit(main())