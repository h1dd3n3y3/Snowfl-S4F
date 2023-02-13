import webbrowser, json, requests, time, msvcrt, csv, os, datetime, clipboard, qbittorrent
from pynput.keyboard import Key, Controller

def chwin(delay):
    keyboard.press(Key.alt)
    time.sleep(0.1)
    keyboard.press(Key.tab)
    time.sleep(0.1)
    keyboard.release(Key.alt)
    time.sleep(0.1)
    keyboard.release(Key.tab)
    time.sleep(delay)

def find_in_browser(keyword):
    keyboard.press(Key.ctrl)
    time.sleep(0.1)
    keyboard.press('f')
    time.sleep(0.1)
    keyboard.release(Key.ctrl)
    time.sleep(0.1)
    keyboard.release('f')
    time.sleep(0.1)

    if keyword == "next": # Focus on the next "1080p" film
        keyboard.press(Key.enter)
        time.sleep(0.1)
        keyboard.release(Key.enter)
        time.sleep(0.1)
    else:
        keyboard.type(keyword)
        time.sleep(0.1)
    
    keyboard.press(Key.esc)
    time.sleep(0.1)
    keyboard.release(Key.esc)
    time.sleep(0.1)

def open_in_browser(url, delay):
    webbrowser.open(url)
    time.sleep(delay)

def type_sortBySeed_go(keyword, delay):
    keyboard.type(keyword)
    time.sleep(0.1)

    for i in range(2):
        keyboard.press(Key.tab)
        time.sleep(0.1)
        keyboard.release(Key.tab)
        time.sleep(0.1)
    
    keyboard.press(Key.right)
    time.sleep(0.1)
    keyboard.release(Key.right)
    time.sleep(0.1)
    keyboard.press(Key.enter)
    time.sleep(0.1)
    keyboard.release(Key.enter)
    time.sleep(delay)

def read_config(filename):
    try:
        with open(filename, "r") as f:
            config = json.load(f)
    except:
        config = None

    return config

def movie_opt():
    print("Select search option for \""+ keyword +"\":\n\n1. Movie.\n2. Subtitles.\n3. Movie & Subtitles.\n0. Re-enter movie keywords.\n\nSpace. Check if torrent available.\nEsc. Exit.\n----------------------------------\nPress one of the above buttons:")
    return str(msvcrt.getch().decode("utf-8")) # Get pressed button

def watchlist_part1(url):
    i = 0;

    # Redownload and refresh IMDb watchlist
    response = requests.get(url)
    open("./init_watchlist.csv", "wb").write(response.content)

    with open("./init_watchlist.csv", 'r') as f:
        with open("./watchlist.csv", 'w') as f1:
            next(f) # skip header line
            for line in f:
                f1.write(line)

    os.remove("./init_watchlist.csv") # Delete old watchlist csv
    f = open("./watchlist.csv", "r+", encoding="utf-8") # Open the watchlist csv
    csv_reader = csv.reader(f) # Read the watchlist csv

    for row in csv_reader:
        if row[8] != "": # Exclude non-released movies
            i += 1

            m_duration = int(row[-6]) % 60
            h_duration_even = int(row[-6]) - m_duration
            h_duration = int(int(h_duration_even) / 60)
            
            if m_duration == 0:
                time_duration = str(h_duration) + "h"
            else:
                time_duration = str(h_duration) + "h-" + str(m_duration) + "m"

            movieList.append(row[5] + " " + row[-5])
            ratingList.append(row[8] + "/10  --  " + time_duration + "  --  "  + row[-4])
            day_monthList.append(datetime.datetime.strptime(row[-2], "%Y-%m-%d").strftime("%d-%b-%Y")[0:6])

    f.close()
    movieList.reverse()
    ratingList.reverse()
    day_monthList.reverse()

    return i

def watchlist_part2(i):
    while 1:
        for a in range(i):
            print(str(a + 1) + ". " + movieList[a] + " (" + day_monthList[a] + ")  --  " + ratingList[a])
        
        print("\n0. Jump back to enter movie keywords.")
        watchlistSelection = (input("---------------------------------------\nChoose a movie number (1-" + str(i) + "): "))

        if watchlistSelection == "":
            os.system("cls")
            print("+------------------------+\n|!! No movie selected. !!|\n|--> Please try again <--|\n+------------------------+\n")
        elif int(watchlistSelection) == 0:
            os.system("cls")
            return "back"
        elif int(watchlistSelection) < 0 or int(watchlistSelection) > i:
            os.system("cls")
            print("+--------------------------+\n|!! Wrong button pressed !!|\n|---> Please try again <---|\n+--------------------------+\n")
        else:
            return movieList[int(watchlistSelection) - 1]

#? <======================= MAIN APP =======================>
movieList = []
ratingList = []
day_monthList = []
keyboard = Controller()
config = read_config("config.json") # Collection of config options included in the config.json file

if config != None:
    if config["IMDb_wlist_exp_link"] != "" or str(config["IMDb_wlist_exp_link"]).endswith("/export"): # Check config file for watchlist export link
        tot_mov = watchlist_part1(config["IMDb_wlist_exp_link"]) # Declare and save watchlist's total movie number

#* <======================= MAIN LOOP =======================>
while 1:
    os.system("cls")

    if config != None:
        if "tot_mov" in vars(): # Checks if "tot_mov" is declared/defined
            keyword = "back"

            while keyword == "back":
                keyword = input("Enter movie keywords (or leave blank & press enter to show IMDb watchlist):\n")
                
                if not keyword: # Empty keyword (pressed enter)
                    os.system("cls")
                    keyword = watchlist_part2(tot_mov)
        else:
            keyword = input("Enter movie keywords (empty keywords are not allowed):\n")

            if not keyword: # If no keyword input (pressed enter)
                continue
    else:
        keyword = input("Enter movie keywords (empty keywords are not allowed):\n")

        if not keyword: # If no keyword input (pressed enter)
            continue

    if config != None:
        if not config["def_search_action"] or config["def_search_action"] == "0": # If default search action not set in config file or set to "0"
            os.system("cls")
            choice = movie_opt() # Show main menu
        else:
            choice = config["def_search_action"]
    else:
        os.system("cls")
        choice = movie_opt() # Show main menu

    #! <======================= CHOICE LOOP =======================>
    while 1:
        if choice == "1": # Movie Search (1 button pressed)
            open_in_browser("https://snowfl.com", 4)
            type_sortBySeed_go(keyword, 3)
            find_in_browser("1080p")

            raise SystemExit(0)
        elif choice == "2": # Subtitles Search (2 button pressed)
            open_in_browser("https://www.subs4free.club/search_report.php?search=" + keyword + "&searchType=1", 0)

            raise SystemExit(0)
        elif choice == "3": # Movie & Subtitles Search (3 button pressed)
            open_in_browser("https://www.subs4free.club/search_report.php?search=" + keyword + "&searchType=1", 2)
            open_in_browser("https://snowfl.com", 2)

            for i in range(2):
                chwin(0.1)
            
            type_sortBySeed_go(keyword, 3)
            find_in_browser("1080p")

            raise SystemExit(0)
        elif choice == "0": # Go back to keyword input (0 button pressed)
            os.system("cls")
            break
        elif choice == " ": # Testing if movie torrnet exists (space button pressed)
            os.system("cls")
            temp = keyword
            open_in_browser("https://snowfl.com", 4)
            type_sortBySeed_go(keyword, 3)
            find_in_browser("1080p")
            chwin(0.1)
            keyword = input("Movie keywords (Press enter to skip to search options):\n")

            if not keyword: # Empty new keyword (pressed enter)
                keyword = temp

            choice = movie_opt() # Show main menu
        elif choice.encode(encoding = 'UTF-8') == b'\x1b': # Exit (escape key pressed)
            raise SystemExit(0)
        else:
            os.system("cls")
            print("+--------------------------+\n|!! Wrong button pressed !!|\n|---> Please try again <---|\n+--------------------------+\n")
            choice = movie_opt() # Show main menu
