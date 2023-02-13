# Snowfl-S4F
Python application for torrent & subtitle movie browser, using keystroke injection, currently targeted for **_WINDOWS 10+_** versions.  
If this **_PATENT_** works, then it provides:  
- Publicly available torrent browser
- 90% Greek and 10% English subtitle content
- Movie selection from IMDb watchlist
- No Custom DNS required
- Script variable pass from JSON file  

It depends on a time delay before executing every action, so the speeds are adjusted for the mid-range **_WINDOWS 10+_** computer.
## Ready Release
Grab the latest from [releases](https://github.com/tru3w1tn3ss/Snowfl-S4F/releases).  

**REMEMBER:** 
- Both _.exe_ and _.json_ files must be in the same folder.
- Follow the [steps below](https://github.com/tru3w1tn3ss/Snowfl-S4F/blob/master/README.md#imdb-watchlist-integration-optional) to include your watchlist link.
## Manual Release (in case of source code modifications)
### Requirements
- #### Python first of all
  - Keep `python` and `pip` version up-to-date.
  - Downlaod windows installer form [here](https://www.python.org/downloads/windows).
- #### Python libraries
  - **EITHER** pip install the libraries:  
  
    `pynput` `requests` `datetime`  
    `pyinstaller` (convert py to exe)  
    `clipboard` `qbittorrent` (currently unnecessary)  
  - **OR** run, in terminal (might need an administrative one):
    ```
    pip install -r requirements.txt
    ```
    inside the cloned repository directory.  
- #### IMDb Watchlist integration _(optional)_
  - Publicly available Watchlist: IMDb web login -> Watchlist -> Edit -> Settings -> Privacy: "Public".
  - Right-click & copy the `Export this list` link.
  - Paste the Watchlist link in the `config.json` file `IMDb_wlist_exp_link` value **_(Double quoted)_**.
### Custom Configuration using config.json file _(optional)_
- Save default search action, after movie title entry/selection, saving time from pressing a last search option button.  
- Edit `config.json` file's `def_search_action` value with the desired option **_(Double quoted)_**.
- The `config.json` file is not required for script execution, making it standalone.
### Windows installation
- Assuming python3 latest version & required libraries are installed.
- In a terminal type:
  ```
  pyinstaller --onefile --icon=.\icon\Movies.ico --paths=C:\python3dir\Lib\site-packages .\Snowfl-S4F.py -y
  ````
  - `pyinstaller`: Python library used to convert _.py_ to _.exe_ files.
  - `--onefile`: Keep all script's libraries inside the exe.
  - `--icon`: Optionally give a custom app icon, followed by it's path (.ico file).
  - `--paths`: There's a chance it might be necessary to point pyinstaller to the python libraries folder.
  - `.\Snowfl-S4F`: The python script itself.
  - `-y`: Consent to every prompt pyinstaller might ask.
- Using config.json _(optional)_:  
  Make sure to have both _.exe_ and _.json_ files in the same folder.
- Enjoy!
