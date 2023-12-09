import os, winreg, webbrowser, datetime, time, msvcrt, shutil #
from sys import exit                                          # Built-in
import win32api, win32gui, win32con      #
import requests, qbittorrentapi, langid  #
import csv, json, configparser           # 3rd-party
from bs4 import BeautifulSoup            #
import keyboard, clipboard               #

def center_win():
    if config != None and config["ui"]["window"]["centered"]:
        console_handle = win32gui.GetForegroundWindow() # Get the handle to the console window

        # Get the screen size
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)

        # Get the work area size, which excludes the taskbar
        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(console_handle, win32con.MONITOR_DEFAULTTONEAREST))
        work_area_rect = monitor_info.get("Work")
        work_area_width = work_area_rect[2] - work_area_rect[0]
        work_area_height = work_area_rect[3] - work_area_rect[1]

        # Get the window size
        window_rect = win32gui.GetWindowRect(console_handle)
        window_width = window_rect[2] - window_rect[0]
        window_height = window_rect[3] - window_rect[1]

        # Calculate the position to center the window on the screen, excluding the taskbar
        pos_x = work_area_rect[0] + (work_area_width - window_width) // 2
        pos_y = work_area_rect[1] + (work_area_height - window_height) // 2

        # Move the window to the center of the screen, excluding the taskbar
        win32gui.MoveWindow(console_handle, pos_x, pos_y, window_width, window_height, True)

def wrap_around_text(rows, cols): # Wrap window around text
    size = shutil.get_terminal_size() # Get the current console window size

    # Prevent excessively small resizing
    if size.columns > cols: cols = size.columns
    if size.lines > rows: rows = size.lines

    os.system(f"mode con cols={cols} lines={rows}")

def press_any_key(msg, prmt_msg): # Custom "pause" message
    print(f"""{msg}
        \rPress any key to {prmt_msg} . . .""")
    os.system("pause >nul")

def wrong_input_box(msg): # Wrong input box dialogue
    if msg != "Wrong button pressed":
        wrap_around_text(tot_mov + 10, len(max(movieDetails, key=len)))
        
    print(f"""+--------------------------+
        \r|!! {msg} !!|
        \r|---> Please try again <---|
        \r+--------------------------+\n""")

def close_tab(delay=0): # Close tab shortcut
    keyboard.press_and_release("ctrl+w")
    time.sleep(delay)

def change_win(delay=0, option=None): # Change window shortcut
    if option == None:
        keyboard.press_and_release("alt+tab")
    elif option == "next": # Focus on the 2nd window in row (the app itself)
        keyboard.press("alt")
        
        for i in range(2):
            keyboard.press_and_release("tab")
            time.sleep(0.1)
        
        keyboard.release("alt")
    
    time.sleep(delay)

def ping_req(hostname): # Ping requests
    if hostname == "google.com":
        os.system("cls")
        print("Checking internet access . . .")

    try:
        response = requests.head(f"https://{hostname}", timeout=5)
        print("Connected!")
        return True
    except:
        return False

def find_in_browser(keyword): # Find in browser shortcut
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

    print(f"'{link}' : {type(link)}")
    if link != " ":
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
        print("torrent auto-selection fail")
        os.system("cls")
        change_win()
        press_any_key("snowfl.com didn't load on time . . .", "retry after snowfl.com has fully loaded")
        change_win(0.1)
        find_in_browser("next")
        save_add_magnet_link()

def copy_link_to_clip(delay): # Copy url link to clipboard
    keyboard.press_and_release("shift+f10")
    time.sleep(0.1)

    if browser == "chrome":
        keyboard.press_and_release("e") # 'Shift + F10' shortcut and then 'E' key
    elif browser == "firefox":
        keyboard.press_and_release("l") # 'Shift + F10' shortcut and then 'L' key
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

        if default_browser in ['chrome', 'firefox', 'Launcher']:
            return default_browser
        else:
            press_any_key(f'"{default_browser} not supported yet . . .', "continue")
            return "unsupported"
    except WindowsError:
        return "Unknown"

def get_default_bittorrent_client_path(): # Get default bittorrent client path
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\Magnet\shell\open\command") as key:
            bittorrent_client = winreg.QueryValue(key, None)
            start = bittorrent_client.find('"') + 1
            end = bittorrent_client.find('"', start)
            bittorrent_client_path = bittorrent_client[start:end]
        
        return bittorrent_client_path
    except WindowsError:
        return "Unknown"

def qbittorrent_webui_actions(): # qBittorrent monitoring
    name, ext = os.path.splitext(os.path.basename(get_default_bittorrent_client_path())) # Save bittorrent client name

    if name == "qbittorrent":
        in_once = 1

        if config != None:
            if not config["torrent"]["qbittorrent"]["monitor_timeout"]:
                max_cnt = 6 # Default timeout evaluates to 5 (sleep time) * 6 (max_cnt) = 30
            else:
                max_cnt = config["torrent"]["qbittorrent"]["monitor_timeout"] // 5 # timeout floor division to multiple of 5 (sleep time)
        
        qbt_config_file = os.path.join(os.getenv("APPDATA"), "qBittorrent", "qBittorrent.ini") # Locate qbittorrent config file

        qbt_config = configparser.ConfigParser()    # 
        qbt_config.read(qbt_config_file)            # Read qbittorrent config

        if qbt_config != None and (web_ui_enabled := qbt_config.getboolean("Preferences", "WebUI\\Enabled")): # Check qbtittorrent config & if WebUI is enabled
            if not (localhost_auth := qbt_config.getboolean("Preferences", "WebUI\\LocalHostAuth")): # Check if localhost authentication bypass is enabled
                if (qbt_client := qbittorrentapi.Client(host="localhost", port=qbt_config.getint("Preferences", "WebUI\\Port"))).is_logged_in: # Check login status
                    while 1:
                        torrents = qbt_client.torrents_info() # Get torrents list:

                        for t in torrents:
                            if t.state in ["stalledUP", "uploading"]: # Finished downlaoding
                                if config["torrent"]["qbittorrent"]["on_download"]["delete_torrent"]:
                                    t.delete(t.hash) # Delete torrent

                                if config["torrent"]["qbittorrent"]["on_download"]["close_window"]:
                                    close_bittorrent_on_finish(get_default_bittorrent_client_path()) # Close qbittorrent window

                                if config["torrent"]["qbittorrent"]["on_download"]["open_torrent_folder"]:
                                    torrent_path = t.content_path

                                    if not keyword.split()[0] in torrent_path:
                                        os.system(f"cd {torrent_path} && mkdir {t.name}")
                                        torrent_path = "{torrent_path}\{t.name}"

                                    os.system(f'explorer.exe "{torrent_path}"') # Open torrent folder

                                return
                            else:
                                if in_once or intr:
                                    intr = 0
                                    in_once = 0
                                    cnt = 0

                                    os.system("cls")
                                    print("""Monitoring qBittorrent . . .\n
                                        \rThis window will stay open until the download is finished.
                                        \rIf you close it manually, any qbittorrent actions will be ignored.\n
                                        \rPlease wait patiently . . .""")
                                
                                time.sleep(5)
                                break # Request agian for torrent info, taking into consideration only the 1st from the list
                        else:
                            cnt += 1

                            if cnt < max_cnt: # Timeout not yet reached (30 sec by default)
                                if cnt == 1:
                                    intr = 1 # Iterruption happened

                                    os.system("cls")
                                    print("No active torrents yet . . .")
                                    print("Listening . . .")
                                time.sleep(5)
                            else: # Break after timeout
                                os.system("cls")
                                press_any_key(f"{cnt * 5}-second timeout reached . . .\nNo active torrent found . . .", "exit")
                                exit(0)
                else:
                    os.system("cls")
                    change_win("next")
                    press_any_key("Failed to authenticate with qBittorrent WebUI . . .", "exit")
            else:
                os.system("cls")
                change_win("next")
                press_any_key("Localhost authentication bypass is disabled . . .", "exit")
        else:
            os.system("cls")
            change_win("next")
            press_any_key("QBittorrent WebUI not enabled . . .", "exit")

def close_bittorrent_on_finish(bittorrent_client_path): # Close bittorrent client on torrent download finish
    name, ext = os.path.splitext(os.path.basename(bittorrent_client_path))

    def find_torrent_window(hwnd, _): # Find bittorrent client window process
        window_title = win32gui.GetWindowText(hwnd)

        if window_title.lower().startswith(name.lower()):
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0) # Send "window close" signal

    win32gui.EnumWindows(find_torrent_window, None)

def download_qbittorrent(): # Download qBittorrent
    open_in_browser("https://www.fosshub.com/qBittorrent.html", 4)
    find_in_browser("qBittorrent Windows x64")
    keyboard.press_and_release("esc")
    keyboard.press_and_release("enter")
    close_tab()

def open_in_browser(url, delay=0): # Open url in browser
    webbrowser.open(url)
    time.sleep(delay)

def type_sortBySeed_go(keyword, delay): # Type, sort by seed & search on snowfl.com
    keyboard.write(keyword)

    for i in range(2):
        keyboard.press_and_release("tab")
    
    keyboard.press_and_release("right")
    keyboard.press_and_release("enter")
    time.sleep(delay)

def read_config(filename): # Read config.json preferances
    try:
        with open(filename, "r") as f:
            config = json.load(f)
    except:
        config = None

    return config

def movie_opt(error=None): # Get movie search option from user
    imdb_search = "\n4. Open on IMDb." if keyword in movieList else ""

    if error != "retry":
        os.system("cls")

    print(f'''Select search option for "{keyword}":\n
        \r1. Movie.
        \r2. Subtitles.
        \r3. Movie & Subtitles.'''
        + imdb_search +
        '''\n0. Re-enter movie keywords.\n
        \rSpace. Check if torrent available.
        \rEsc. Exit.
        \r----------------------------------
        \rPress one of the above buttons:''')

    return str(msvcrt.getch().decode("utf-8")) # Get pressed button

def check_eng_title(title): # Check if IMDb watchlist.csv title is enlish
    lang, prop = langid.classify(title)

    return True if lang == "en" else False

def get_eng_title(link): # Get IMDb english title from link
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US"}

    try:
        response = requests.get(f"https://www.imdb.com/title/{link}", headers=headers)
    except:
        press_any_key("No internet connection . . .", "exit")

    html = BeautifulSoup(response.content, "html.parser")
    movie_title = html.find("h1").text

    return movie_title

def watchlist_part1(watchlist_url): # Watchlist backend
    i = 0;

    try: # Get watchlist request
        os.system("cls")
        print("Fetching IMDb watchlist . . .")
        response = requests.get(watchlist_url)
    except:
        return False

    with open("./init_watchlist.csv", "wb") as init_watch: # Now save the request as a file
        init_watch.write(response.content)
    
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

            m_duration = int(row[-6]) % 60              #
            h_duration_even = int(row[-6]) - m_duration # Get time duration
            h_duration = int(int(h_duration_even) / 60) #
            
            time_duration = str(h_duration) + 'h'

            if m_duration != 0:
                time_duration += ' ' + str(m_duration) + 'm'
            
            movieTitle = row[5]
            
            #Translate non-english titles takes too long, so leave it for now
            #
            # if not check_eng_title(movieTitle): # Check if title is english
            #     if in_once:
            #         os.system("cls")
            #         print("Translating non-english titles . . .")
            #         in_once = 0
                
            #     movieTitle = get_eng_title(row[1]) # Convert title to english
            #     if movieTitle.lower() != row[5].lower():
            #         print(f'"{row[5]}" --> "{movieTitle}"')
            #     else:
            #         movieTitle = row[5]
            
            movieList.append(f"{movieTitle} {row[-5]}") # Save movie & year
            imdbLinkList.append(f"https://www.imdb.com/title/{row[1]}") # Save IMDb movie link
            ratingList.append(f"{row[8]}/10 ({time_duration}) -- {row[-4]}")
            dayMonthList.append(datetime.datetime.strptime(row[-2], "%Y-%m-%d").strftime("%d-%b-%Y")[0:6])

    f.close()

    for list in movieList, imdbLinkList, ratingList, dayMonthList:
        list.reverse()

    return i # Get total movie number

def watchlist_part2(i): # Watchlist frontend
    movieDetails = [(f"{a+1}. {movieList[a]} ({dayMonthList[a]}) -- {ratingList[a]}") for a in range(i)]
    
    wrap_around_text(i + 5, len(max(movieDetails, key=len)))
    center_win()

    while 1:
        for m in range(i):
            print(movieDetails[m])

        print("""\n0. Jump back to enter movie keywords.
            \r---------------------------------------\n""")
        watchlistSelection = (input(f"Choose a movie number (1-{i}): "))

        if not watchlistSelection:
            os.system("cls")
            wrong_input_box(" No movie selected  ")
        elif int(watchlistSelection) == 0: # Re-enter movie keywords
            os.system("cls")
            return "back"
        elif 0 > int(watchlistSelection) > i: # Number out of range
            os.system("cls")
            wrong_input_box("Wrong number pressed")
        else:
            return movieList[int(watchlistSelection) - 1] # Get movie & year

#? <=========================== MAIN APP ==========================>

config = read_config("config.json") # Collection of config options included in the config.json file
center_win() # Center terminal window
movieList = []
imdbLinkList = []
ratingList = []
dayMonthList = []
movieDetails = []
clipboard.copy(" ") # Generate a blank clipboard copied text

while 1:
    if config != None:
        if config["browser"]["IMDb_watchlist_export_link"].endswith("/export")\
        and (tot_mov := watchlist_part1(config["browser"]["IMDb_watchlist_export_link"])):
            break # IMDb watchlist fetched successfully / Connected to internet
        else:
            if not ping_req("google.com"): # Check internet connection
                press_any_key("No internet connection . . .", "retry")
            else:
                break # Connected to internet
    else:
        if not ping_req("google.com"): # Check internet connection
            press_any_key("No internet connection . . .", "retry")
        else:
            break # Connected to internet

if (bittorr_cli := get_default_bittorrent_client_path()) == "Unknown":
    print("""No Bittorrent client installed . . .
        \rDownload qBittorrent (recommended) and continue?(y/n)""")
    if msvcrt.getch().decode("utf-8") == 'y':
        download_qbittorrent()
    else:
        exit(0)

if (browser := get_default_browser()) == "unsupported":
    print("Browser", browser)

#* <========================== MAIN LOOP ==========================>

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
            choice = movie_opt() # Show main menu
    else: # If config file is not present
        choice = movie_opt() # Show main menu

    #! <======================= CHOICE LOOP =======================>

    while 1:
        if choice in ['1', ' ']:
            open_in_browser("https://snowfl.com", 5)
            type_sortBySeed_go(keyword, 3)

            if config != None and (value := config["browser"]["find_in_page"]):
                find_in_browser(value)

            if choice == '1': # Movie Search (1 button pressed)
                if config != None and (value := config["browser"]["find_in_page"]) and config["torrent"]["auto_select"]:
                    manget_link = save_add_magnet_link()
                    qbittorrent_webui_actions()

                exit(0)
            else: # Check if movie torrnet exists (space button pressed)
                os.system("cls")
                change_win(0.1)
                temp = keyword
                keyword = input("Movie keywords (Press enter to skip to search options):\n")

                if not keyword: # Empty new keyword (pressed enter)
                    keyword = temp

                choice = movie_opt() # Show main menu
        elif choice in  ['2', '3', '4']:
            if choice in ['2', '3']:
                open_in_browser(f"https://www.subs4free.club/search_report.php?search={keyword}\
                    &searchType=1", 0 if choice == '2' else 2) # Subtitles Search (2 button pressed)

                if choice == '3': # Movie & Subtitles Search (3 button pressed)
                    open_in_browser("https://snowfl.com", 2)

                    for i in range(2):
                        change_win(0.5)
                    
                    type_sortBySeed_go(keyword, 3)

                    if config != None and (value := config["browser"]["find_in_page"]):
                        find_in_browser(value)

                        if config["torrent"]["auto_select"]:
                            magnet_link = save_add_magnet_link()
                            qbittorrent_webui_actions()

                exit(0)    
            else: # IMDb search (4 button pressed)
                open_in_browser(imdbLinkList[movieList.index(keyword)])
                choice = movie_opt() # Show main menu
        elif choice == '0': # Go back to keyword input (0 button pressed)
            break
        elif choice.encode(encoding = "UTF-8") == b'\x1b': # Exit (escape key pressed)
            exit(0)
        else:
            os.system("cls")
            wrong_input_box("Wrong button pressed")
            choice = movie_opt("retry") # Show main menu
