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

def ItemMenu(station):
    curses.endwin()
    os.system('clear')
    week_playlist.save_playlist(station)
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
    myscreen.addstr(9, 1,  "  9 - All radiostation")
    myscreen.addstr(10, 1, "  0 - Exit")
    myscreen.addstr(11, 1, "========================================")
    myscreen.addstr(12, 1, "  Enter a selection: ")
    myscreen.refresh()


def MainInKey():
    key = 'X'
    while key != ord('0'):
        key = myscreen.getch(12, 22)
        myscreen.addch(12, 22, key)

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

        # elif key == ord('4'):
        #     myscreen.erase()
        #     myscreen.addstr(1, 1, "========================================")
        #     myscreen.addstr(2, 1, "    Playlist for LUX not done           ")
        #     myscreen.addstr(3, 1, "========================================")
        #     myscreen.addstr(10, 1, "   Press a key :")
        #     myscreen.refresh()
        #     myscreen.getch()
        #     DoMainMenu()

        elif key == ord('9'):
            curses.endwin()
            os.system('clear')
            week_playlist.save_playlist('hit_fm')
            week_playlist.save_playlist('kiss_fm')
            week_playlist.save_playlist('rus_radio')
            week_playlist.save_playlist('lux_fm')
            week_playlist.save_playlist('nrj_fm')
            input("Done, press Enter to continue...")
            DoMainMenu()
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
