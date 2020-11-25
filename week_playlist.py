#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import lxml.html as html
import os
import csv
import json
from urllib.request import urlopen, Request as URL_Request
import threading
import time


#from collections import OrderedDict

'''
If need add new station firs off all add it to get url and after that to  get_playlist
'''


def get_week():
    # Get dates of previous week
    week_dates = []
    today = datetime.date.today()
    weekday = today.weekday()
    start_delta = datetime.timedelta(days=weekday, weeks=1)
    start_of_week = today - start_delta

    for day in range(7):
        week_dates.append(start_of_week + datetime.timedelta(days=day))

    return week_dates


def get_url(station_name):

    template_url = {
        "hit_fm"    : ('https://www.hitfm.ua/playlist/*.html', '%d-%m-%Y'),
        "kiss_fm"  : ('https://www.kissfm.ua/playlist/*.html', '%d-%m-%Y'),
        "rus_radio" : ('https://www.rusradio.ua/playlist/*.html', '%d-%m-%Y'),
        # 'lux_fm'   : ('http://www.moreradio.org/playlist_radio/radio_lux_fm/*/#H14', '%d_%B_%Y'),
        'lux_fm': ('https://lux.fm/music/archive/get-songs-html?dateStr=*&datePeriodIndex=#', '%Y-%m-%d'),
        'nrj_fm'    : ('https://nrj.ua/programs/playlist?date=*&time_start=00:00&time_stop=23:59&p=#', '%d.%m.%Y'),
        # 'dj_fm'     : ('http://radioscope.in.ua/paging.php?s=djfm&date=*', '%Y/%m/%d/#'),
        'dj_fm'     : ('https://dancemelody.ru/plsajax/ajaxpost.php?*', '%Y-%m-%d'),
        'power_fm'  : ('https://radiovolna.net/radio_stations/stations/by-day.html?*', '%Y-%m-%d'),
        'maximum_fm': ('https://maximum.fm/get-more-archive/4/*%2000:00/*%2023:59', '%Y-%m-%d'),

    }

    urls = {}
    for day in get_week():
        urls[day] = (template_url[station_name][0].replace('*', day.strftime(template_url[station_name][1]).lower()),
                     station_name)
    return urls


def get_playlist(address,  pl_folder, pl_file, station_):

    if not os.path.isdir(pl_folder):
        print('*** Make folder ', pl_folder)
        os.makedirs(pl_folder)

    with open(os.path.join(pl_folder, pl_file), 'w', newline='') as csv_pl:
        print('*** Make file ', pl_file)
        csvwriter = csv.writer(csv_pl, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        # HIT FM
        if station_ == 'hit_fm':
            print('*** Get html page ', address)
            page = html.parse(urlopen(address))
            l = page.getroot().find_class('song-list')
            for i in l:
                Time = i.find_class('stl-absolute date-podcast').pop().text_content()
                Artist = i.find_class('sing-name').pop().text_content().replace('\n', '')
                Song = i.find_class('song-name').pop().text_content().replace('\n', '')
                csvwriter.writerow((Time, Artist, Song))


        # Russ RADIO
        elif station_ == "rus_radio":
            print('*** Get html page ', address)
            page = html.parse(urlopen(address))
            # print(page.getroot().text_content())
            l = page.getroot()
            for j in l.find_class('d-flex'):
                # print(html.tostring(j))
                Time = j.find_class('blue-date left').pop().text_content()
                Artist = j.find_class('artist').pop().text_content().replace('\n', '')
                Song = j.find_class('song_playlist').pop().text_content().replace('\n', '')
                csvwriter.writerow((Time, Artist, Song))


        # LUX FM from site
        elif station_ == "lux_fm":
            for period in (0, 1, 2, 3, 4,):
                addr = address.replace('#', str(period))
                print('*** Get html page ', addr)
                req = URL_Request(addr, headers={'User-Agent': 'Mozilla/5.0'})
                page = html.parse(urlopen(req))
                pl = json.loads(page.getroot().text_content())
                l = html.document_fromstring(pl['html']).find_class('song-wrapper-bg')
                if not l:
                    continue
                for item in l:
                    Time = item.find_class('time').pop().text_content().strip()
                    Song = item.find_class('song-name').pop().text_content().strip()
                    Artist = item.find_class('song-artist').pop().text_content().strip()
                    # print(Time, Artist, Song)
                    csvwriter.writerow((Time, Artist, Song))


        # KISS FM
        elif station_ == "kiss_fm":
            print('*** Get html page ', address)
            try:
                page = html.parse(urlopen(address))
                l = page.getroot().find_class('playlist-item')
                for i in l:
                    Time = i.find_class('songTime').pop().text_content()
                    Artist = i.find_class('artist').pop().text_content().replace('\n', '')
                    Song = i.find_class('song').pop().text_content().replace('\n', '')
                    csvwriter.writerow((Time, Artist, Song))
            except OSError:
                print('!!! Error get ', address)
                csvwriter.writerow(('!!! Error get ' + address, ''))


        # NRJ
        elif station_ == "nrj_fm":
            songs = set()
            for i in range(1, 19):
                addr = address.replace('#', str(i))
                print('*** Get html page ', addr)
                page = html.parse(urlopen(addr))
                l = page.getroot().find_class('jp_container')
                for j in l:
                    Time = j.find_class('time').pop().text_content().strip()
                    Title = j.find_class('jp-title').pop().text_content().strip()
                    Artist = j.find_class('title').pop().text_content().strip()
                    Song = Title.replace(Artist, '').strip()
                    if Song:
                       songs.add((Time, Artist, Song))

            for j in sorted(songs):
                csvwriter.writerow(j)


        # MAXIMUM_FM
        elif station_ == "maximum_fm":
            for hours in (('00:00', '07:00'),
                                ('07:00', '11:00'),
                                ('11:00', '15:00'),
                                ('15:00', '21:00'),
                                ('21:00', '23:59')):
                addr = address.replace('00:00', hours[0]).replace('23:59', hours[1])
                print('*** Get html page ', addr)
                req = URL_Request(addr, headers={'User-Agent': 'Mozilla/5.0'})
                # page = html.parse(urlopen(addr))
                page = html.parse(urlopen(req))
                pl = json.loads(page.getroot().text_content())
                # print(pl)
                if not pl['playlist']:
                    continue
                for row in pl['playlist']:
                    # print(row.keys())
                    Time = datetime.datetime.fromtimestamp(row['onAirDate']).strftime('%Y-%m-%d %H:%M')
                    Artist = row['artists'][0]['name']
                    Song = row['name']

                    csvwriter.writerow((Time, Artist, Song))

        # DJ_FM
        elif station_ == "dj_fm":
            import urllib.request
            import urllib.parse
            print('*** Get html page ', address)
            data = urllib.parse.urlencode({'search_term': address.split('?')[1], 'pls': 'djfm'})
            data = data.encode('ascii')
            with urllib.request.urlopen(address.split('?')[0], data) as f:
                page = html.parse(f)
                l = page.getroot().text_content()
                pls = [i.strip() for i in l.splitlines() if i.strip()]
                for pls_item in pls:
                    # print(pls_item)
                    try:
                        Artist = pls_item.split(' - ')[-1].strip()
                        Time = pls_item.split(' - ')[-2].strip()[:5]
                        Song = pls_item.split(' - ')[-2].strip()[8:]
                    except IndexError:
                        Artist = ""
                        Time = ""
                        Song = ""
                    # print(Time, Artist, '-', Song)
                    csvwriter.writerow((Time, Artist.title(), Song.title()))

        # POWER_FM
        elif station_ == "power_fm":
            import urllib.parse
            from urllib.request import Request

            print('*** Get html page ', address)
            data_day = address.split('?')[1]
            url_addr = address.split('?')[0]
            data = urllib.parse.urlencode({'stationId': '14', 'day': data_day}).encode('ascii')
            ques = Request(url_addr, data=data, headers={ 'X-Requested-With': 'XMLHttpRequest'})

            with urlopen(ques) as f:
                pl = json.loads((f.read()).decode('utf8'))
                # print(pl)
                if pl['data']:
                    page = html.document_fromstring(pl['data'])
                    for row in page.find_class('item'):
                        # print(html.tostring(row))
                        Time = row.find_class('time').pop().text_content()
                        Title = row.find_class('item-title').pop().text_content().strip()
                        Artist = Title.split('-')[0].strip()
                        Song = Title.split('-')[1].strip()

                        csvwriter.writerow((Time, Artist.title(), Song.title()))
                else:
                    csvwriter.writerow(('No data on site',))


        # Unknown radio
        else:
            return -1

        # Print how many song found
        with open(csv_pl.name, "r") as f:
            written_lines = len(f.readlines())
            if written_lines <= 1:
                print('!!!! Empty playlist!')
            else:
                print('**** Songs written to file = \"%d\"' % (written_lines))

def save_playlist(st):
    print()
    print('* Getting playlist for ', st.upper())
    print()
    for pl in get_url(st).items():
        file_name = pl[0].strftime('%Y-%m-%d(%a)') + pl[1][1] + '.csv'
        week_folder = 'Week_#' + str(pl[0].isocalendar()[1])
        dir_name = os.path.join(week_folder, pl[1][1].upper() + '_week#' + str(pl[0].isocalendar()[1]))
        station = pl[1][1]
        pl_url = pl[1][0]
        # Catch all exception
        try:
            get_playlist(pl_url, dir_name, file_name, station)
        except Exception as my_error:
            print(my_error)


if __name__ == "__main__":

    enable_tread = True
    start_time = time.time()
    radio_stations = ('hit_fm',
                     'kiss_fm',
                     'lux_fm',
                     'nrj_fm',
                     'dj_fm',
                     'power_fm',
                     'maximum_fm',
                     'rus_radio',
                     )
    threads = []
    for station in radio_stations:
        print('Start for station: {}'.format(station))
        if enable_tread:
            tr = threading.Thread(target=save_playlist, args=(station,))
            tr.start()
            threads.append(tr)
        else:
            save_playlist(station)

    # join all threads
    for tr in threads:
        tr.join()

    print("Done in : ", time.time() - start_time)
