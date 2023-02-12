# Snowfl-S4F
Python application for torrent & subtitle movie browser, using keystroke injection, currently targeted for **_WINDOWS 10+_**.  
If this **_PATENT_** works, then it provides:  
- Publicly available torrent browser
- 1080p torrent quality, find-in-page functionality
- 90% Greek and 10% English subtitle content
- No Custom DNS required
- Script variable pass from JSON file  

It depends on a time delay before executing every action, so the speeds are adjusted for the mid-range **_WINDOWS 10+_** computer.
## Requirements
- ### Python first of all
  - Keep `python` and `pip` version up-to-date.
- ### Python libraries
  - **EITHER** pip install the libraries:  
  
    `pynput` `requests` `datetime`  
    `clipboard` `qbittorrent` (currently unnecessary)  
  - **OR** run, in terminal:
    ```
    pip -r install requirements.txt
    ```
    inside the cloned repository directory.  
- ### IMDb Watchlist integration _(optional)_
  - Publicly available Watchlist: IMDb web login -> Watchlist -> Edit -> Settings -> Privacy: "Public".
  - Right-click & copy the `Export this list` link.
  - Insert the Watchlist link in the `config.json` file `IMDb_wlist_exp_link` value **_(Double quoted)_**.
## Bonus
- Save favorite search action, after movie title entry/selection, saving time from pressing a last search option button.  
- Edit `config.json` file `def_search_action` value with the desired option **_(Double quoted)_**.
