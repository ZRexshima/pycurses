import curses
import requests


def get_new_joke():
    joke_json = requests.get('https://api.chucknorris.io/jokes/random')
    if joke_json.status_code == 200:
        json = joke_json.json()
        return json['value']


def main(wrapper):

    stdscr = curses.initscr()

    curses.noecho()
    curses.cbreak()

    # Hide cursor
    curses.curs_set(0)

    # Check for and begin color support
    if curses.has_colors():
        curses.start_color()

    # Add color combos
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    # Begin pgm
    stdscr.addstr("RANDOM QUOTES", curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

    stdscr.addstr(curses.LINES-1, 0, "Press 'R' to request a new quote, 'Q' to quit")

    # Change the R to green
    stdscr.chgat(curses.LINES-1, 7, 1, curses.A_BOLD | curses.color_pair(2))

    # Change the Q to red
    stdscr.chgat(curses.LINES-1, 35, 1, curses.A_BOLD | curses.color_pair(1))

    # Create a window to hold the quotes
    quote_window = curses.newwin(curses.LINES-2, curses.COLS, 1, 0)

    # Create a sub-window so as to cleanly display a quote without
    # worrying about overwriting the quote window's borders
    quote_text_window = quote_window.subwin(curses.LINES-6, curses.COLS-4, 3, 2)


    quote_text_window.addstr("Press 'R' to get your first quote!")

    # Draw a boirder around the main quote window
    quote_window.box()

    # Update the internal window data structures
    stdscr.noutrefresh()
    quote_window.noutrefresh()

    # Redraw the screen
    curses.doupdate()

    # Create the event loop
    while True:
        c = quote_window.getch()

        if c == ord('r') or c == ord('R'):  # I want to change this to use .lower
            quote_text_window.clear()
            quote_text_window.addstr("Getting quote...", curses.color_pair(3))

            quote_text_window.refresh()
            quote_text_window.clear()
            quote_text_window.addstr(get_new_joke())

        elif c == ord('q') or c == ord('Q'):
            break

        # Refresh the windows from the bottom up
        stdscr.noutrefresh()
        quote_window.noutrefresh()
        quote_text_window.noutrefresh()
        curses.doupdate()


curses.wrapper(main)
