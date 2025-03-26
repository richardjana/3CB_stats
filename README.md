# 3CB stats


## frontend
All information on the current 3CB league:
* Hall of Fame, player statistics etc.
* detailed information on every round
* API documentation


## API
* serves the underlying data to authorized users
* includes scripts for scraping new rounds and processing the data



* properly log all API requests with user_name:
    app.logger.info('%s failed to log in', user.username)
    (https://flask.palletsprojects.com/en/stable/logging/)
* save card data from scryfall in local storage
