# Snowfl-S4F
Python application for torrent & subtitle movie browsing, using keystroke injection.  
## <ins>**!! DISCLAIMER !!**</ins>
- **_ONLY_** for <ins>**_WINDOWS 10+_**</ins> versions.
- **_ONLY_** for <ins>**supported**</ins> browsers.  
- A <ins>**Bittorrent client**</ins> is <ins>**required**</ins> _(duh...)_: [**_qBittorrent_**](https://www.fosshub.com/qBittorrent.html) is recommended, but everything else is fine _(€$£)_.

### If this <ins>_BODGE_</ins> works, then it provides:  
- Publicly available torrent browser
- Find-in-page 1080p torrents
- Automatic torrent downlaod _(optionally)_
- 90% Greek and 10% English subtitle content browser
- No DNS restrictions _(currently)_
- [**_IMDb WATCHLIST_**](https://github.com/h1dd3n3y3/Snowfl-S4F/blob/master/README.md#imdb-watchlist-integration-optional) movie selection _(optionally)_
- [**JSON Custom Configuration**](https://github.com/h1dd3n3y3/Snowfl-S4F/blob/master/README.md#custom-configuration-using-configjson-file-optional)  

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
    
    using pip:
    ```
    pip install <lib_name>
    ```
  - **OR** run:
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
## <ins>IMDb Watchlist integration</ins> _(optional)_
  - Publicly available Watchlist: IMDb web login -> Watchlist -> Edit -> Settings -> Privacy: "Public".
  - Right-click & copy the `Export this list` link.
  - Paste the Watchlist link in the `config.json` file.
## <ins>Custom Configuration using config.json file</ins> _(optional)_
- ### Both <ins>_.exe_ and _.json_ files</ins> must be <ins>in the same folder</ins> _(if planning to use the config.json)_.
- ### <ins>Every value</ins> must be <ins>**_double quoted_**</ins> after each option name, <ins>except</ins> for those with <ins>**_boolean_**</ins> values (JSON Logic).
- ### JSON Mapping:
  - IMDb Watchlist: `IMDb_watchlist_export_link` to export link **_(ending with "/export")_**.
  - Default search action, after movie title entry/selection: `default_search_action` between `1-3`.
  - Auto torrent selection: `auto_select` to `true/false` or leave empty.
  - Auto close browser tab after torrent added: `close_tab_after_torrent_add` to `true/false` or leave empty.
  - Open Bittorrent client, (just in case it won't launch automatically): `open_bittorrent_client_after` to `true/false` or leave empty.
