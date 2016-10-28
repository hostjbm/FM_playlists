#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import lxml.html as html
import os
import csv

'''
If need add new station firs off all add it to get url and after that to  get_playlist
'''

def get_week():
    # Get date of previous week
    week_dates = []
    today = datetime.date.today()
    # today = datetime.date(2016, 9, 14)
    weekday = today.weekday()
    start_delta = datetime.timedelta(days=weekday, weeks=1)
    start_of_week = today - start_delta

    for day in range(7):
        week_dates.append(start_of_week + datetime.timedelta(days=day))

    return week_dates


def get_url(station__):
    urls = {}

    if station__ == "hit_fm":
        template = 'http://www.hitfm.ua/playlist/*.html'
    elif station__ == "kiss_fm":
        template = 'http://www.kissfm.ua/playlist/*.html'
    elif station__ == "rus_radio":
        template = 'http://www.rusradio.ua/playlist/*.html'

    # LUX FM
    elif station__ == 'lux_fm':
        template = 'http://www.moreradio.org/playlist_radio/radio_lux_fm/*/#H14'
        for day in get_week():
            urls[day] = (template.replace('*', day.strftime('%d_%B_%Y').lower()), station__)
        return urls

    elif station__ == 'nrj_fm':
        template = 'http://nrj.ua/programs/playlist?date=*&time_start=00:00&time_stop=23:59&p=#'
        for day in get_week():
            urls[day] = (template.replace('*', day.strftime('%d.%m.%Y').lower()), station__)
        return urls

    else:
        print("!!!!! Unknown station !!!!!!!!!!!")
        return -1

    for day in get_week():
        urls[day] = (template.replace('*', day.strftime('%d-%m-%Y')), station__)
    return urls
    ############################################


def get_playlist(address,  pl_folder, pl_file, station_):

    if pl_folder not in os.listdir('.'):
        print('*** Make folder ', pl_folder)
        os.mkdir(pl_folder)

    with open(os.path.join(pl_folder, pl_file), 'w', newline='') as csv_pl:
        print('*** Make file ', pl_file)
        csvwriter = csv.writer(csv_pl, delimiter=';', quoting=csv.QUOTE_MINIMAL)

        # HIT FM
        if station_ == 'hit_fm':
            print('*** Get html page ', address)
            page = html.parse(address)
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
            page = html.parse(address)
            l = page.getroot()
            for i in range(0, 330):
                try:
                    song = l.get_element_by_id('ss' + str(i))
                    Time = song.find_class('blue-date').pop().text_content()
                    Artist = song.find_class('artist').pop().text_content().replace('\n', '')
                    Song = song.find_class('song_playlist').pop().text_content().replace('\n', '')
                    csvwriter.writerow((Time, Artist, Song))
                except KeyError:
                    continue
            return 0


        # LUX FM
        elif station_ == "lux_fm":
            import urllib.request

            print('*** Get html page ', address)
            opener = urllib.request.build_opener()
            opener.addheaders.append(('Cookie', 'AllTrackRadio=563'))
            f = opener.open(address)
            page = html.parse(f)
            l = page.getroot().find_class('plItemGrey')
            for i in l:
                try:
                    Time = i.find_class('time').pop().text_content().strip()
                    Title = i.find_class('MiddleBlack').pop().text_content()
                    Song = i.find_class('MiddleBlack').pop().text

                    Time = Time[:2] + ':' + Time[2:]
                    Artist = Title.replace(Song, '')

                    # print(Time, Artist, Song)
                    csvwriter.writerow((Time, Artist, Song))
                except IndexError:
                    continue

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


        # Unknown radio
        else:
            return -1


def save_playlist(st):
    print()
    print('* Getting playlist for ', st.upper())
    print()
    for pl in get_url(st).items():
        file_name = pl[0].strftime('%Y-%m-%d(%a)') + pl[1][1] + '.csv'
        dir_name = pl[1][1].upper() + '_week#' + str(pl[0].isocalendar()[1])
        station = pl[1][1]
        pl_url = pl[1][0]
        get_playlist(pl_url, dir_name, file_name, station)



if __name__ == "__main__":

    # save_playlist('rus_radio')
    # save_playlist('hit_fm')
    save_playlist('kiss_fm')
    # save_playlist('lux_fm')


    # print(get_url('nrj_fm'))
    # save_playlist('nrj_fm')




    # get_playlist('http://lux.fm/player/airArchive.do?filter=2016090700', 'TEST', 'test.csv', "lux_fm")