import os, winreg, webbrowser, datetime, time, msvcrt # Built-in libraries
from bs4 import BeautifulSoup                   #
import requests, qbittorrentapi, langid         # 3rd-party libraries
import csv, json, configparser                  #
import win32gui, win32con, keyboard, clipboard  #

def press_any_key(msg, prmt_msg):
    print(f"""{msg}
        \rPress any key to {prmt_msg} . . .""")
    os.system("pause >nul")

def wrong_input_box(msg):
    print(f"""+--------------------------+
        \r|!! {msg} !!|
        \r|---> Please try again <---|
        \r+--------------------------+\n""")

def close_tab(delay):
    keyboard.press_and_release("ctrl+w")
    time.sleep(delay)

def change_win(delay, option = None):
    if option == None:
        keyboard.press_and_release("alt+tab")
    elif option == "next":    
        keyboard.press("alt")
        
        for i in range(2):
            keyboard.press_and_release("tab")
            time.sleep(0.1)
        
        keyboard.release("alt")
    
    time.sleep(delay)

def ping_req(hostname):
    if hostname == "google.com":
        os.system("cls")
        print("Checking internet access . . .")

    try:
        response = requests.head(f"https://{hostname}", timeout=5)
        print("Connected!")
        return True
    except:
        return False

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

def save_add_magnet_link(): # Save magnet link
    keyboard.press_and_release("tab")
    time.sleep(0.1)
    copy_link_to_clip(0.1)
    link = clipboard.paste()

    if link.startswith("http") or link.startswith("magnet"):
        if not link.startswith("magnet"):
            if link.endswith("/#fetch"):
                find_in_browser("next")
                
            save_add_magnet_link()
        else:
            open_in_browser(link, 0.1)

            if config != None: # If config exists
                if config["browser"]["close_tab_after_torrent_add"]:
                    close_tab(0.1) # Close browser tab
                if config["torrent"]["auto_launch_client"]:
                    os.system(f'cmd /c "{bittorr_cli}"') # Launch bittorrent client
    else:
        os.system("cls")
        change_win(0)
        press_any_key(f'No "{keyword}" torrents found . . .', "exit")

def copy_link_to_clip(delay): # Save url link
    keyboard.press_and_release("shift+f10")
    time.sleep(0.1)

    if browser == "chrome": # 'Shift + F10' shortcut and then 'E' key
        keyboard.press_and_release("e")
    elif browser == "firefox": # 'Shift + F10' shortcut and then 'L' key
        keyboard.press_and_release("l")
    elif browser == "Launcher": # Opera browser
        for i in range(5):
            keyboard.press_and_release("down")

        keyboard.press_and_release("enter")

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

def get_default_bittorrent_client_path():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\Magnet\shell\open\command") as key:
            bittorrent_client = winreg.QueryValue(key, None)
            start = bittorrent_client.find('"') + 1
            end = bittorrent_client.find('"', start)
            bittorrent_client_path = bittorrent_client[start:end]
        
        return bittorrent_client_path
    except WindowsError:
        return "Unknown"

def qbittorrent_webui_actions():
    name, ext = os.path.splitext(os.path.basename(get_default_bittorrent_client_path())) # Save bittorrent client name

    if name == "qbittorrent":
        qbt_config_file = os.path.join(os.getenv("APPDATA"), "qBittorrent", "qBittorrent.ini") # Locate qbittorrent config file

        qbt_config = configparser.ConfigParser()    # 
        qbt_config.read(qbt_config_file)            # Read qbittorrent config

        if qbt_config != None and (web_ui_enabled := qbt_config.getboolean("Preferences", "WebUI\\Enabled")): # Check qbtittorrent config & if WebUI is enabled
            if not (localhost_auth := qbt_config.getboolean("Preferences", "WebUI\\LocalHostAuth")): # Check if localhost authentication bypass is enabled
                if (qbt_client := qbittorrentapi.Client(host="localhost", port=qbt_config.getint("Preferences", "WebUI\\Port"))).is_logged_in: # Check the login status
                    os.system("cls")
                    print("""Downloading torrent . . .\n
                        \rqBittorrent is being currently monitored . . .
                        \rThis window will stay open until the download is finished.
                        \rIf you close it manually, any qbittorrent actions will be ignored.\n
                        \rPlease wait patiently . . .""")

                    while 1:
                        torrents = qbt_client.torrents_info() # Get torrents list

                        for t in torrents:
                            if t.state == "stalledUP":
                                if config["torrent"]["qbittorrent"]["on_download"]["delete_torrent"]:
                                    t.delete(t.hash) # Delete torrent

                                if config["torrent"]["qbittorrent"]["on_download"]["close_window"]:
                                    close_bittorrent_on_finish(get_default_bittorrent_client_path()) # Close qbittorrent window

                                if config["torrent"]["qbittorrent"]["on_download"]["open_torrent_folder"]:
                                    torrent_path = t.content_path
                                    os.system(f'explorer.exe "{torrent_path}"') # Open torrent folder

                                return
                            else:
                                break # Request agian for torrent info, taking into consideration only the 1st from the list
                        else:
                            print("No active torrents")
                            break

                        time.sleep(5)
                else:
                    os.system("cls")
                    change_win(0, "next")
                    press_any_key("Failed to authenticate with qBittorrent WebUI . . .", "exit")
            else:
                os.system("cls")
                change_win(0, "next")
                press_any_key("localhost authentication bypass is disabled . . .", "exit")
        else:
            os.system("cls")
            change_win(0, "next")
            press_any_key("qBittorrent WebUI not enabled . . .", "exit")

def close_bittorrent_on_finish(bittorrent_client_path):
    name, ext = os.path.splitext(os.path.basename(bittorrent_client_path))

    def find_torrent_window(hwnd, _):
        window_title = win32gui.GetWindowText(hwnd)

        if window_title.lower().startswith(name.lower()):
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    win32gui.EnumWindows(find_torrent_window, None)

def download_qbittorrent():
    open_in_browser("https://www.fosshub.com/qBittorrent.html", 4)
    find_in_browser("qBittorrent Windows x64")
    keyboard.press_and_release("esc")
    keyboard.press_and_release("enter")
    close_tab(0)

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
    print(f'''Select search option for "{keyword}":\n
        \r1. Movie.
        \r2. Subtitles.
        \r3. Movie & Subtitles.
        \r0. Re-enter movie keywords.\n
        \rSpace. Check if torrent available.
        \rEsc. Exit.
        \r----------------------------------
        \rPress one of the above buttons:''')

    return str(msvcrt.getch().decode("utf-8")) # Get pressed button

def check_eng_title(title):
    lang, prop = langid.classify(title)

    if lang == "en":
        return True
    else:
        return False

def get_eng_title(link):
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US"}

    response = requests.get(f"https://www.imdb.com/title/{link}", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    movie_title = soup.find("h1").text

    return movie_title

def watchlist_part1(watchlist_url):
    i = 0;

    # watchlist download
    try:
        os.system("cls")
        print("Getting IMDb watchlist . . .")
        response = requests.get(watchlist_url)
    except:
        return False
    open("./init_watchlist.csv", "wb").write(response.content)

    try:
        with open("./init_watchlist.csv", 'r') as f_old:
            with open("./watchlist.csv", 'w') as f_new:
                next(f_old) # skip header line

                for line in f_old:
                    f_new.write(line)
    except:
        return "Unknown"

    os.remove("./init_watchlist.csv") # Delete old watchlist csv
    f = open("./watchlist.csv", "r+", encoding="utf-8") # Open the watchlist csv
    csv_reader = csv.reader(f) # Read the watchlist csv
    in_once = 1

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
            
            movieTitle = row[5]
            
            if not check_eng_title(movieTitle): # Check if title is english
                if in_once:
                    os.system("cls")
                    print(f'Translating non-english watchlist titles . . .')
                    in_once = 0
                
                movieTitle = get_eng_title(row[1]) # Convert title to english
                if movieTitle != row[5]:
                    print(f'"{row[5]}" --> "{movieTitle}"')
            
            movieList.append(movieTitle + " " + row[-5])
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
        
        print("""\n0. Jump back to enter movie keywords.
            \r---------------------------------------\n""")
        watchlistSelection = (input("Choose a movie number (1-" + str(i) + "): "))

        if watchlistSelection == "":
            os.system("cls")
            wrong_input_box(" No movie selected  ")
            
        elif int(watchlistSelection) == 0:
            os.system("cls")
            return "back"
        elif 0 > int(watchlistSelection) > i:
            os.system("cls")
            wrong_input_box("Wrong number pressed")
        else:
            return movieList[int(watchlistSelection) - 1]

#? <======================= MAIN APP =======================>
config = read_config("config.json") # Collection of config options included in the config.json file
movieList = []
ratingList = []
day_monthList = []

while 1:
    if config == None or not config["browser"]["IMDb_watchlist_export_link"].endswith("/export")\
        or not (tot_mov := watchlist_part1(config["browser"]["IMDb_watchlist_export_link"])):
            if not ping_req("google.com"): # Check internet connection
                press_any_key("No internet connection . . .", "retry")
    else:
        break

if (bittorr_cli := get_default_bittorrent_client_path()) == "Unknown":
    print("""No Bittorrent client installed . . .
        \rDownload qBittorrent (recommended) and continue?(y/n)""")
    if msvcrt.getch().decode("utf-8") == 'y':
        download_qbittorrent()
    else:
        raise SystemExit(0)

browser = get_default_browser()

#* <======================= MAIN LOOP =======================>
while 1:
    os.system("cls")

    if config != None: # If config file is present
        if "tot_mov" in vars(): # If "tot_mov" is declared/defined == config watchlist can be used
            keyword = "back"

            while keyword == "back":
                keyword = input("Enter movie keywords (leave empty for IMDb watchlist):\n")
                
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
        if config["browser"]["default_search_action"] in range(1, 4): # If default search action not between 1-3
            choice = str(config["browser"]["default_search_action"])
        else:
            os.system("cls")
            choice = movie_opt() # Show main menu
    else: # If config file is not present
        os.system("cls")
        choice = movie_opt() # Show main menu

    #! <======================= CHOICE LOOP =======================>
    while 1:
        if choice == '1': # Movie Search (1 button pressed)
            open_in_browser("https://snowfl.com", 4)
            type_sortBySeed_go(keyword, 3)
            find_in_browser("1080p")

            if config != None and config["torrent"]["auto_select"]:
                manget_link = save_add_magnet_link()
            
            qbittorrent_webui_actions()

            raise SystemExit(0)
        elif choice == '2': # Subtitles Search (2 button pressed)
            open_in_browser(f"https://www.subs4free.club/search_report.php?search={keyword}&searchType=1", 0)

            raise SystemExit(0)
        elif choice == '3': # Movie & Subtitles Search (3 button pressed)
            open_in_browser(f"https://www.subs4free.club/search_report.php?search={keyword}&searchType=1", 2)
            open_in_browser("https://snowfl.com", 2)

            for i in range(2):
                change_win(0.2)
            
            type_sortBySeed_go(keyword, 3)
            find_in_browser("1080p")

            if config != None and config["torrent"]["auto_select"]:
                magnet_link = save_add_magnet_link()

            qbittorrent_webui_actions()

            raise SystemExit(0)
        elif choice == '0': # Go back to keyword input (0 button pressed)
            os.system("cls")
            break
        elif choice == ' ': # Testing if movie torrnet exists (space button pressed)
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
        elif choice.encode(encoding = "UTF-8") == b'\x1b': # Exit (escape key pressed)
            raise SystemExit(0)
        else:
            os.system("cls")
            wrong_input_box("Wrong button pressed")
            choice = movie_opt() # Show main menu
