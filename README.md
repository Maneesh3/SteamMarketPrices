# SteamMarketPrices

This python code retrives the steam market prices of products provided the steam market URL's.

## Telegram Bot :robot:
Added Telegram Bot, which interacts with users to retrive the prices from links from users.

**Telegram Bot folder -**
* `config.json` contains Bot API key, MongoDB config details
* `dbHandler.py` for database entry, updation, deletion
* `priceBot.py` main bot program

## Requirements
* `Python 3.7`
  * `json`
  * `urllib.request`
  * `urllib.parse`

## working
* run the program using `python price.py`
* `list.txt` file contains all the product URL's from Steam Market seperated in each line

```
with example link output is:
★ Falchion Knife | Blue Steel (Field-Tested)
₹ 7,000.14
```
## To-Do
- [x] Display the prices
- [ ] Database MongoDB to store each users watchlist links   [*__currently developing__*]
- [ ] Custom currency to choose from
- [ ] Alert sent to Telegram using a bot, when price is low at a certain point
- [ ] Release this project as a bot for multiple users with database
