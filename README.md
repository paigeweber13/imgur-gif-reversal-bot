# TODO:
* [x] put everything from manual test together into end_to_end
* [x] write script that does everything from the command line
* [x] put script on server with cronjob to run it regularly (how often to not go
      over API limit?)
      * [x] how many requests per run of 'bot_cli.py'?
* [x] how to avoid duplicates? Look for comments with same name I guess? Wait a
      long time so we can be reasonably sure that there are only new posts?
* [ ] rewrite readme now that this is basically finished

# Notes
## Authorization
### Resources:
https://api.imgur.com/oauth2
https://apidocs.imgur.com/?version=latest#register-an-application-important

## Imgur API
### Rate limiting
12,500 post requests per day
uploads count as 10 requests

24 hours in a day
approx. 500 requests per hour
     or 50  uploads per hour

which is one upload per 1.2 minutes (1 minutes 12 seconds)

### Number of calls I make
Requests in each call of comment_reversed_gif_on_all_rising_gifs
 * max 50 times (if every post is a gif)
   * 10 calls used for upload
   * 1 call for making comment

for each call, we have worst case of 550 calls, which is more than what we are
allowed to do in an hour. Only allowed about 500. Waiting 1hour 15minutes would
amount to 10,560 calls in a day, which is well below the limit. is 1:15 long
enough for posts to all be new?
