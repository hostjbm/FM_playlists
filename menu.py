#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
import curses
import week_playlist
import os
import datetime

PYTHONDONTWRITEBYTECODE=1

Current_day = datetime.date.today().strftime('week#%W    %d-%b-%Y')

def ItemMenu(stations):
    curses.endwin()
    os.system('clear')
    if type(stations) == tuple:
        for station in stations:
            week_playlist.save_playlist(station)
    else:
        week_playlist.save_playlist(stations)
    input("Done, press Enter to continue...")
    DoMainMenu()


def DoMainMenu():
    myscreen.erase()
    myscreen.addstr(0, 1,  "Current date:     " + Current_day        )
    myscreen.addstr(1, 1,  "========================================")
    myscreen.addstr(2, 1,  "           Get week playlist            ")
    myscreen.addstr(3, 1,  "========================================")
    myscreen.addstr(4, 1,  "  1 - HIT FM")
    myscreen.addstr(5, 1,  "  2 - KISS FM")
    myscreen.addstr(6, 1,  "  3 - Rus radio")
    myscreen.addstr(7, 1,  "  4 - Lux FM")
    myscreen.addstr(8, 1,  "  5 - NRJ FM (P.S Need run on monday, as early as possible)")
    myscreen.addstr(9, 1,  "  6 - DJ FM")
    myscreen.addstr(10, 1, "  7 - POWERFM")
    myscreen.addstr(11, 1, "  9 - All radio station")
    myscreen.addstr(12, 1, "  0 - Exit")
    myscreen.addstr(14, 1, "========================================")
    myscreen.addstr(15, 1, "  Enter a selection: ")
    myscreen.refresh()


def MainInKey():
    key = 'X'
    while key != ord('0'):
        key = myscreen.getch(15, 22)
        myscreen.addch(15, 22, key)

        if key == ord('1'):
            ItemMenu('hit_fm')

        elif key == ord('2'):
            ItemMenu('kiss_fm')

        elif key == ord('3'):
            ItemMenu('rus_radio')

        elif key == ord('4'):
            ItemMenu('lux_fm')

        elif key == ord('5'):
            ItemMenu('nrj_fm')

        elif key == ord('6'):
            ItemMenu('dj_fm')

        elif key == ord('7'):
            ItemMenu('power_fm')

        elif key == ord('9'):
            ItemMenu(('hit_fm', 'kiss_fm', 'rus_radio', 'lux_fm', 'nrj_fm', 'dj_fm', 'power_fm'))

        myscreen.refresh()


def LogicLoop():
    DoMainMenu()
    MainInKey()

#  MAIN LOOP
try:
    myscreen = curses.initscr()
    LogicLoop()
finally:
    curses.endwin()
