# SteamMarketPrices

This python code retrives the steam market prices of products provided the steam market URL's.

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
- [ ] Database MongoDB to store each users watchlist links
- [ ] Custom currency to choose from
- [ ] Alert sent to Telegram using a bot, when price is low at a certain point
- [ ] Release this project as a bot for multiple users with database
