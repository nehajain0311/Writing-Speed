import curses #https://docs.python.org/3/howto/curses.html
from curses import wrapper #this wrapper takes command of windows terminal over and its commands, it initialis curses module
import time
import random

#create a start screen which clears it self from the beginning and add welcomes ask us to enter by hitting any key
#create a wrapper function which check if key entered is esc or backspace else add the key to a user input list
    #also create target text list
    #runs continuosly till user say esc
    #on backspace delete the char just entered by user
    #clear screen
    #create a function to display the target text and overlay text as user type
# create a display function:
    #display target text
    #as user types run for loop to check user input and write it, for every char the cycle runs that many times from
        #--wrapper function to display function as character added to the userinput list
        #inside for loop character is checked if its correct, display green color, starting on 0th row to overlay,
         #and index same as target text
        #for wrong text color is red





def start_screen(stdscr): # we need to pass thid object because we are printing and modifyin on screen
    stdscr.clear()  # clear screen from before
    stdscr.addstr("Welcome to the Speed Test!")
    stdscr.addstr("\nPress any key to begin")
    # to include color add parameter color_pair or its optional argument
    # if we add row, column before our text (2,0, hello world) --> 2nd row, and column 0 postion
    stdscr.refresh()  # it refreshes the screen
    stdscr.getkey()  # it just waits for the user for any input , we can store this input too to check what user i

def load_text():
    with open("text.txt","r")as f:
        lines=f.readlines()
        return random.choice(lines).strip()



def display_text(stdscr,target_text,current_text,wpm=0): #this is going to create overlay

    stdscr.addstr(target_text,curses.color_pair(3))  # this will display target text on screen,

    for i,char in enumerate(current_text):# this forloop continuosly add th overlay till the user inputs
        correct_text = target_text[i] #target text char
        if correct_text==char:
            stdscr.addstr(0,i,char, curses.color_pair(2)) #0th row means same as target row, and index as moves as user input
        else:
            stdscr.addstr(0,i,char,curses.color_pair(1)) #wrong will print in red color
    stdscr.addstr(1,0,f"WPM: {wpm}")



def wpm_test(stdscr): #target text
    target_text=load_text()
    current_text=[]
    start_time=time.time()
    stdscr.nodelay(True) #this will not let user stay waiting long

    # create the overlay text of user going to type over it
    while True:
        elapsed_time=max((time.time()-start_time),1) #time elapsed will be more than the startime but it could be less than a minute so we can use max functinon if the evalation is negative or zero it will  print 1

        #(elasped_time/60) --->per minute time conversion
        #char/per minute= len(current_tex)/(elapsed_time/60)
        # words per minute == 5 words per minute (usually or that's how calculated)
        wpm=round(len(current_text)/(elapsed_time/60)/5)

        stdscr.clear()  # we have to clear screen, as the for loop continuaoly add text on next line on each key input
        display_text(stdscr,target_text,current_text,wpm) #call th function after clear
        stdscr.refresh()

        if "".join(current_text)==target_text: #current_text is a list, so to compare it needs to convert in string
            stdscr.nodelay(False) #this will stop the wpm timer and let the user enter key
            break #breaks the while loop
        try:
             key=stdscr.getkey() #if user doenot enter anything, because of stdcrs.nodelay() throws error
        except:
            continue

        if ord(key) == 27:  # escape characters ordinal key
            break
        if key in ('KEY_BACKSPACE','\b','\x7f'): #theses are backspace representation on diff sytem
                # when backspace delete char
            if len(current_text)>0:
                current_text.pop() #delete char
        elif len(current_text)<len(target_text):
                current_text.append(key) #if not then only we are adding char to current_text
                # add the key to list of user input


def main(stdscr): #stdscr for standard screen
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # to create coloured text we have to create color pair: foreground color + background color
    # this is only possible inside the function which is initialised by wrapper
    #(id of pair,foreground color,backgroun color)

    #stdscr.addstr("Hello world!",curses.color_pair(2))
    #to include color add parameter color_pair or its optional argument
    #if we add row, column before our text (2,0, hello world) --> 2nd row, and column 0 postion

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2,0,"You comleted the task, enter any key to continue")
        key=stdscr.getkey()
        if ord(key) ==27:
            break

wrapper(main) #pass the function to wrapper, it intitalies curser on that function, and clears once function stops
