#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import lxml.html as html
import os
import csv
import json
from urllib.request import urlopen
#from collections import OrderedDict

'''
If need add new station firs off all add it to get url and after that to  get_playlist
'''


def get_week():
    # Get dates of previous week
    week_dates = []
    today = datetime.date.today()
    # today = datetime.date(2016, 9, 14)
    weekday = today.weekday()
    start_delta = datetime.timedelta(days=weekday, weeks=1)
    start_of_week = today - start_delta

    for day in range(7):
        week_dates.append(start_of_week + datetime.timedelta(days=day))

    return week_dates


def get_url(station_name):

    template_url = {
        "hit_fm"    : ('https://www.hitfm.ua/playlist/*.html', '%d-%m-%Y'),
        "kiss_fm"   : ('http://www.kissfm.ua/playlist/*.html', '%d-%m-%Y'),
        "rus_radio" : ('https://www.rusradio.ua/playlist/*.html', '%d-%m-%Y'),
        # 'lux_fm'    : ('http://www.moreradio.org/playlist_radio/radio_lux_fm/*/#H14', '%d_%B_%Y'),
        'lux_fm':    ('http://dancemelody.ru/plsajax/ajaxpost.php?*', '%Y-%m-%d'),
        'nrj_fm'    : ('http://nrj.ua/programs/playlist?date=*&time_start=00:00&time_stop=23:59&p=#', '%d.%m.%Y'),
        'dj_fm'     : ('http://radioscope.in.ua/paging.php?s=djfm&date=*', '%Y/%m/%d/#')

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
                Time = i.find_class('songTime').pop().text_content()
                Artist = i.find_class('sing-name').pop().text_content().replace('\n', '')
                Song = i.find_class('song-name').pop().text_content().replace('\n', '')
                csvwriter.writerow((Time, Artist, Song))
            return 0

        # KISS FM
        elif station_ == "kiss_fm":
            print('*** Get html page ', address)
            try:
                page = html.parse(address)
                l = page.getroot().find_class('playlist-item')
                for i in l:
                    Time = i.find_class('songTime').pop().text_content()
                    Artist = i.find_class('artist').pop().text_content().replace('\n', '')
                    Song = i.find_class('song').pop().text_content().replace('\n', '')
                    csvwriter.writerow((Time, Artist, Song))
            except OSError:
                print('!!! Error get ', address)
                csvwriter.writerow(('!!! Error get ' + address, ''))
            return 0

        # Russ RADIO
        elif station_ == "rus_radio":
            print('*** Get html page ', address)
            page = html.parse(urlopen(address))
            #print(page.getroot().text_content())
            l = page.getroot()
            for j in l.find_class('fd'):
                try:
                    Time = j.text_content().strip()
                    id = j.getchildren().pop().get('id')
                    id = id[1:] # del first char in Time id 
                    #print(Time, id)
                    Artist = l.get_element_by_id(id).find_class('artist').pop().text_content()
                    Song = l.get_element_by_id(id).find_class('song_playlist').pop().text_content()
                    csvwriter.writerow((Time, Artist, Song))
                except KeyError:
                    continue

            return 0

        # LUX FM
        elif station_ == "lux_fm":
            import urllib.request
            import urllib.parse
            print('*** Get html page ', address)
            data = urllib.parse.urlencode({'search_term': address.split('?')[1], 'pls': 'songs89'})
            data = data.encode('ascii')
            with urllib.request.urlopen(address.split('?')[0], data) as f:
                page = html.parse(f)
                l = page.getroot().text_content()
                pls = [i.strip() for i in l.splitlines() if i.strip()]
                for pls_item in pls:
                    # print(pls_item)
                    Artist = pls_item.split(' - ')[-1].strip()
                    Time = pls_item.split(' - ')[-2].strip()[:5]
                    Song = pls_item.split(' - ')[-2].strip()[8:]
                    # print(Time, Artist, '-', Song)
                    csvwriter.writerow((Time, Artist.title(), Song.title()))

            # From MORERADIO

            # import urllib.request
            # print('*** Get html page ', address)
            # opener = urllib.request.build_opener()
            # opener.addheaders.append(('Cookie', 'AllTrackRadio=563'))
            # f = opener.open(address)
            # page = html.parse(f)
            # l = page.getroot().find_class('plItemGrey')
            # for i in l:
            #     try:
            #         Time = i.find_class('time').pop().text_content().strip()
            #         Title = i.find_class('MiddleBlack').pop().text_content()
            #         Song = i.find_class('MiddleBlack').pop().text
            #
            #         Time = Time[:2] + ':' + Time[2:]
            #         Artist = Title.replace(Song, '')
            #
            #         # print(Time, Artist, Song)
            #         csvwriter.writerow((Time, Artist, Song))
            #     except IndexError:
            #         continue

        # NRJ
        elif station_ == "nrj_fm":
            songs = set()
            for i in range(1, 19):
                addr = address.replace('#', str(i))
                print('*** Get html page ', addr)
                page = html.parse(addr)
                l = page.getroot().find_class('jp_container')
                for j in l:
                    Time = j.find_class('time').pop().text_content().strip()
                    Title = j.find_class('jp-title').pop().text_content().strip()
                    Artist = j.find_class('title').pop().text_content().strip()
                    Song = Title.replace(Artist, '').strip()
                    if Song:
                       songs.add((Time, Artist, Song))
                    # print(Time, Artist, Song)

            for j in sorted(songs):
                csvwriter.writerow(j)

        # DJ_FM
        elif station_ == "dj_fm":
            # make url for each hour
            for i in range(1, 24, 2):
                addr = address.replace('#', str(i))
                print('*** Get html page ', addr)
                page = html.parse(addr)
                pl = json.loads(page.getroot().text_content())
                # from dict to list and reverse sorting
                pl = [i for i in list(pl.items()) if i[0].isdigit()]
                pl.sort(key=lambda x: int(x[0]), reverse=True)

                for row in pl:
                    time_from_json = datetime.datetime.fromtimestamp(row[1]['start'])
                    Time = time_from_json.strftime('%H:%M')
                    Title = row[1]['name'].encode('iso-8859-1').decode('UTF-8')
                    # print(Time, Title)
                    # if in title '-' more then one. They will go to song name
                    Artist, *S = Title.split(' - ')
                    Song = S[0] if len(S) == 1 else ' - '.join(S)

                    csvwriter.writerow((Time, Artist, Song))

        # Unknown radio
        else:
            return -1


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
        get_playlist(pl_url, dir_name, file_name, station)


if __name__ == "__main__":

    save_playlist('rus_radio')
    save_playlist('hit_fm')
    save_playlist('kiss_fm')
    save_playlist('lux_fm')
    save_playlist('nrj_fm')
    save_playlist('dj_fm')

    # print(get_url('dj_fm'))
    # get_playlist('http://lux.fm/player/airArchive.do?filter=2016090700', 'TEST', 'test.csv', "lux_fm")
