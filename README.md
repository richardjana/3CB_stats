# 3CB stats


## frontend
All information on the current 3CB league:
* Hall of Fame, player statistics etc.
* detailed information on every round
* API documentation


## API
* serves the underlying data to authorized users
* includes scripts for scraping new rounds and processing the data


* for each player (or hall of fame as well): plot showing some metric vs. time (probably Elo or choice)
* scrape additional information somehow? (rules, notes, deadlines, etc.)
* update requirements files (especially the python one)
* test replacing pandas with polars: 1) test the speed 2) implement tests beforehand to ensure correctness
* implement tests: assert for python (is there a more proper way for this?); proper testing library for react
