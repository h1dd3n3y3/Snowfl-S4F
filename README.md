# Snowfl-S4F
Python application for torrent & subtitle movie browsing, using keystroke injection.  
## <ins>**!! DISCLAIMER !!**</ins>
- **_ONLY_** for <ins>**_WINDOWS 10+_**</ins> versions.
- **_ONLY_** for <ins>**supported**</ins> browsers.  
- A <ins>**Bittorrent client**</ins> is <ins>**required**</ins> _(duh...)_: [**_qBittorrent_**](https://www.fosshub.com/qBittorrent.html) is recommended, but everything else is fine _(€$£)_.

### If this <ins>LAZY_</ins> <ins>_BODGE_</ins> works, then it provides:  
- Publicly available torrent browser
- Find-in-page 1080p torrents
- Automatic torrent downlaod _(optionally)_
- 90% Greek and 10% English subtitle content browser
- No DNS restrictions _(currently)_
- [**_IMDb WATCHLIST_**](https://github.com/h1dd3n3y3/Snowfl-S4F#imdb-watchlist-integration) movie selection _(optionally)_
- [**_qBittorrent torrent automation_**](https://github.com/h1dd3n3y3/Snowfl-S4F#qbittorrent-integration) _(optionally)_
- [**_JSON Custom Configuration_**](https://github.com/h1dd3n3y3/Snowfl-S4F#custom-configuration-using-configjson-file) _(optionally)_  

### Browser support:  
- Chrome
- Firefox
- Opera

Delay, before every action, adjusted for the average computer.
## <ins>Ready Release</ins>
### Grab the latest one from [**_RELEASES_**](https://github.com/tru3w1tn3ss/Snowfl-S4F/releases).  

## <ins>Manual Release</ins> (code modifications)
### Requirements
- #### Python first of all
  - Keep `python` and `pip` version up-to-date.
  - Downlaod windows installer form [**_HERE_**](https://www.python.org/downloads/windows).
- #### Python libraries
  - **EITHER** install the libraries:  
  
    `keyboard` (keystroke injection)  
    `clipboard` (clipboard access)  
    `requests` (http requests)  
    `pywin32` (window events)  
    `qbittorrent-api` (qbittorrent WebUI remote interraction)  
    `configparser` (qbittorrent config access)  
    `pyinstaller` (_.py_ to _.exe_ conversion)  
    
    manually, by running:
    ```
    pip install <lib_name>
    ```
  - **OR** using the _requirements.txt_ file:
    ```
    pip install -r requirements.txt
    ```
    inside the cloned repository directory.  
    In both cases, you **<ins>might need an administrative shell.</ins>**
### Installation
- In a terminal type:
  ```
  pyinstaller --onefile --icon=.\icon\Movies.ico --paths=<DriveLetter>:\<PythonDir>\Lib\site-packages .\Snowfl-S4F.py -y
  ```
  - `pyinstaller`: Python library used to convert _.py_ to _.exe_ files.
  - `--onefile`: Keep all script's libraries inside the exe.
  - `--icon`: Optionally give a custom app icon, followed by it's path (.ico file).
  - `--paths`: There's a chance it might be necessary to point pyinstaller to the python libraries folder.
  - `.\Snowfl-S4F`: The python script itself.
  - `-y`: Consent to every prompt pyinstaller might ask.
## Optional goodies
## <ins>IMDb Watchlist integration</ins>
  - Publicly available Watchlist: IMDb web login -> `Watchlist` -> `Edit` -> `Settings` -> `Privacy: "Public"`.
  - Right-click & copy the `Export this list` link.
  - Paste the Watchlist link in the `config.json` file.
 ## <ins>qBittorrent integration</ins>
  - WebUI must be enabled: Options -> Web UI -> check Web User Interface (Remote Control) option.
    - Set desired `port` (make sure no other app is using it, mine was VLC)
    - Crucial: check `Bypass authentication for clients on localhost` option.
  - Click: `Apply` -> `OK`.
  - Restart qBittorrent: bottom right `icon tray` -> `right click` -> `exit` -> `relaunch`.
## <ins>Custom Configuration using config.json file</ins>
- ### Both <ins>_.exe_ and _.json_ files</ins> must be <ins>in the same folder</ins> _(if planning to use the config.json)_.
- ### <ins>Every value</ins> must be <ins>**_double quoted_**</ins> after each option name, <ins>except</ins> for those with <ins>**_boolean_**</ins> values (JSON Logic).
### <ins>JSON Mapping</ins>
- #### For everyone:
  - <ins>**IMDb Watchlist:**</ins> `IMDb_watchlist_export_link` to export link **_(ending with "/export")_**.
  - <ins>**Default search action**</ins>, after movie title entry/selection: `default_search_action` between `1-3` **_(0 will be ignored)_**.
  - <ins>**Auto torrent selection:**</ins> `auto_select` to `true/false`.
  - <ins>**Auto close browser tab**</ins>, after auto torrent selection: `close_tab_after_torrent_add` to `true/false`.
  - <ins>**Open Bittorrent client**</ins>, (just in case it won't launch automatically): `auto_launch_client` to `true/false`.
- #### For qBittorrent users, on torrent download finished:
  - <ins>**Delete torrent:**</ins> `delete_torrent` to `true/false`.
  - <ins>**Close qBittorrent window:**</ins> `close_window` to `true/false`.
  - <ins>**Open torrent folder:**</ins> `open_torrent_folder` to `true/false`.
