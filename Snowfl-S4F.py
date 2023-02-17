import os, winreg, webbrowser, datetime, time, msvcrt, keyboard, csv, json, requests, clipboard, qbittorrent

def close_tab():
    if config != None and config["close_tab_after_torrent_add"] == "true":
        keyboard.press_and_release("ctrl+w")

def change_win(delay):
    keyboard.press_and_release("alt+tab")
    time.sleep(delay)

def find_in_browser(keyword):
    keyboard.press_and_release("ctrl+f")
    time.sleep(0.1)

    if keyword == "next": # Focus on the next "1080p" film
        keyboard.press_and_release("enter")
        time.sleep(0.1)
    else:
        keyboard.write(keyword)
        time.sleep(0.1)
    
    keyboard.press_and_release("esc")
    time.sleep(0.1)

def get_and_add_magnet_link(): # Save magnet link
    keyboard.press_and_release("tab")
    time.sleep(0.1)
    copy_link_to_clip(0.1)
    link = clipboard.paste()

    if not link.startswith("magnet"):
        if link.endswith("/#fetch"):
            find_in_browser("next")
            
        get_and_add_magnet_link()
    else:
        open_in_browser(link, 0.1)
        close_tab()

def copy_link_to_clip(delay): # Save url link
    keyboard.press_and_release("shift+f10")
    time.sleep(0.1)

    if browser == "chrome": # 'Shift + F10' shortcut and then 'E' key
        keyboard.press_and_release("e")
    elif browser == "firefox": # 'Shift + F10' shortcut and then 'L' key
        keyboard.press_and_release("l")

    time.sleep(delay)

def get_default_browser(): # Get default browser from Windows Registry
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice") as key:
            prog_id, _ = winreg.QueryValueEx(key, "Progid")

        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, fr"{prog_id}\shell\open\command") as key:
            browser_path, _ = winreg.QueryValueEx(key, "")
            default_browser = os.path.splitext(os.path.basename(browser_path))[0]

        return default_browser
    except WindowsError:
        return "Unknown"


def open_in_browser(url, delay):
    webbrowser.open(url)
    time.sleep(delay)

def type_sortBySeed_go(keyword, delay):
    keyboard.write(keyword)

    for i in range(2):
        keyboard.press_and_release("tab")
    
    keyboard.press_and_release("right")
    keyboard.press_and_release("enter")
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

    try:
        with open("./init_watchlist.csv", 'r') as f:
            with open("./watchlist.csv", 'w') as f1:
                next(f) # skip header line

                for line in f:
                    f1.write(line)
    except:
        return "Unknown"

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
browser = get_default_browser()
config = read_config("config.json") # Collection of config options included in the config.json file

if config != None: # If config file is present
    if config["IMDb_wlist_exp_link"] != "" or str(config["IMDb_wlist_exp_link"]).endswith("/export"): # Check config file for watchlist export link
        tot_mov = watchlist_part1(config["IMDb_wlist_exp_link"]) # Declare and save watchlist's total movie number

#* <======================= MAIN LOOP =======================>
while 1:
    os.system("cls")

    if config != None: # If config file is present
        if "tot_mov" in vars(): # If "tot_mov" is declared/defined == config watchlist can be used
            keyword = "back"

            while keyword == "back":
                keyword = input("Enter movie keywords (or leave blank & press enter to show IMDb watchlist):\n")
                
                if not keyword: # Empty keyword (pressed enter)
                    os.system("cls")
                    keyword = watchlist_part2(tot_mov)
        else:# If "tot_mov" is not declared/defined == config watchlist cannot be used
            keyword = input("Enter movie keywords (empty keywords are not allowed):\n")

            if not keyword: # If no keyword input (pressed enter)
                continue
    else: # If config file is not present
        keyword = input("Enter movie keywords (empty keywords are not allowed):\n")

        if not keyword: # If no keyword input (pressed enter)
            continue

    if config != None: # If config file is present
        if not config["def_search_action"] or config["def_search_action"] == "0": # If default search action not set in config file or set to "0"
            os.system("cls")
            choice = movie_opt() # Show main menu
        else:
            choice = config["def_search_action"]
    else: # If config file is not present
        os.system("cls")
        choice = movie_opt() # Show main menu

    #! <======================= CHOICE LOOP =======================>
    while 1:
        if choice == "1": # Movie Search (1 button pressed)
            open_in_browser("https://snowfl.com", 4)
            type_sortBySeed_go(keyword, 3)
            find_in_browser("1080p")

            if config != None and config["add_torrent_auto"] == "true":
                get_and_add_magnet_link()

            raise SystemExit(0)
        elif choice == "2": # Subtitles Search (2 button pressed)
            open_in_browser("https://www.subs4free.club/search_report.php?search=" + keyword + "&searchType=1", 0)

            raise SystemExit(0)
        elif choice == "3": # Movie & Subtitles Search (3 button pressed)
            open_in_browser("https://www.subs4free.club/search_report.php?search=" + keyword + "&searchType=1", 2)
            open_in_browser("https://snowfl.com", 2)

            for i in range(2):
                change_win(0.1)
            
            type_sortBySeed_go(keyword, 3)
            find_in_browser("1080p")

            if config != None and config["add_torrent_auto"] == "true":
                get_and_add_magnet_link()

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
            change_win(0.1)
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
