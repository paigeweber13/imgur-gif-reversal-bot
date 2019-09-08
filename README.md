# GifReversalBot
A bot that comments on gifs uploaded to imgur with a reversed version of that
gif. Is sometimes funny or entertaining.

# The work of this bot
Want to see it in action? Take a look here:
https://imgur.com/user/GifReversalBot/comments 

# TODO:
* [ ] implement parallelism so that we can gether data on multiple galleries at
  once
* [ ] start gathering data on how new posts are in each gallery and the score
  of posts in each gallery.
* [ ] improve argument handling in cli. Switch to argparse.ArgumentParser

# Notes
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
