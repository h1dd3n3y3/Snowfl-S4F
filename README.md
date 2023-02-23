# Snowfl-S4F
Python application for torrent & subtitle movie browsing, using keystroke injection.  
## <ins>**!! DISCLAIMER !!**</ins>
- **_ONLY_** for <ins>**_WINDOWS 10+_**</ins> versions **_ONLY_**.
- **_ONLY_** for <ins>**supported**</ins> browsers.  
- A <ins>**Bittorrent client**</ins> is <ins>**required**</ins> _(duh...)_: [**_qBittorrent_**](https://www.fosshub.com/qBittorrent.html) is recommended, but everything else is fine _(€$£)_.

### If this <ins>_BODGE_</ins> works, then it provides:  
- Publicly available torrent browser
- Find-in-page 1080p torrents
- Automatic torrent downlaod _(optionally)_
- 90% Greek and 10% English subtitle content browser
- No DNS restrictions _(currently)_
- [**_IMDb WATCHLIST_**](https://github.com/tru3w1tn3ss/Snowfl-S4F/blob/master/README.md#imdb-watchlist-integration-optional) movie selection _(optionally)_
- [**JSON Custom Configuration**](https://github.com/tru3w1tn3ss/Snowfl-S4F#custom-configuration-using-configjson-file-optional)  

### Browser support:  
- Chrome
- Firefox
- Opera

Time delay before every action, adjusted for the average computer.
## <ins>Ready Release</ins>
### Grab the latest one from [**_RELEASES_**](https://github.com/tru3w1tn3ss/Snowfl-S4F/releases).  

## <ins>Manual Release</ins> (code modifications)
### Requirements
- #### Python first of all
  - Keep `python` and `pip` version up-to-date.
  - Downlaod windows installer form [**_HERE_**](https://www.python.org/downloads/windows).
- #### Python libraries
  - **EITHER** _pip-install_ the libraries:  
  
    `keyboard` `requests` `datetime` `clipboard`  
    `pyinstaller` (convert py to exe)  
    `qbittorrent` (currently unnecessary)  
    
    like:
    ```
    pip install <lib_name>
    ```
  - **OR** run, in terminal:
    ```
    pip install -r requirements.txt
    ```
    inside the cloned repository directory.  
    In both cases, you **<ins>might need an administrative shell.</ins>**
- #### IMDb Watchlist integration _(optional)_
  - Publicly available Watchlist: IMDb web login -> Watchlist -> Edit -> Settings -> Privacy: "Public".
  - Right-click & copy the `Export this list` link.
  - Paste the Watchlist link in the `config.json` file `IMDb_wlist_exp_link` value **_(Double quoted)_**.
<<<<<<< HEAD
### Custom Configuration using config.json file _(optional)_
#### - true/false values <ins>MUST NOT</ins> be double quoted

- Save default search action, after movie title entry/selection, saving time from pressing a last search option button.  
- Edit `config.json` file's `default_search_action` value with the desired option .
- Auto torrent download with `true` value in `add_torrent_auto` option **_(Double quoted)_**.
- Auto tab close after torrent addition by setting `true` the value of `close_tab_after_torrent_add` **_(Double quoted)_**.
- The `config.json` file is _not required for script execution_, making it standalone.
### Windows Installation
=======
## <ins>Custom Configuration using config.json file _(optional)_</ins>
- ### Both <ins>_.exe_ and _.json_ files</ins> must be <ins>in the same folder</ins> _(if planning to use the config.json)_.
- ### <ins>Every value</ins> must be <ins>**_double quoted_**</ins> after each option name (JSON Logic):
  - Save default search action, after movie title entry/selection, saving time from pressing a last search option button.  
  - Edit `config.json` file's `def_search_action` value with the desired option (1-3).
  - Auto torrent download with `true` value in `add_torrent_auto`.
  - Auto tab close after torrent addition by setting `true` the value of `close_tab_after_torrent_add`.
  - Open Bittorrent client, just in case it won't launch automatically, with `true` value in `open_bittorrent_client_after`.
  - The `config.json` file is _not required for script execution_, making it standalone.
## <ins>Windows Installation</ins>
>>>>>>> b96eb12812866e3144876c7cc6801135d827bc15
- Assuming python3 latest version & required libraries are installed.
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
- Both _.exe_ and _.json_ files must be in the same folder _(if planning to use the config.json)_.
- **Enjoy!**
