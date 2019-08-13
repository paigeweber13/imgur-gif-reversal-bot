# Notes
## Authorization
### Resources:
https://api.imgur.com/oauth2
https://apidocs.imgur.com/?version=latest#register-an-application-important

## Imgur API
### Getting rising usersub
GET https://api.imgur.com/3/gallery/user/rising/day/1?album_previews=true
interesting parts of call:
data is array of posts

data[0].title
data[0].is_ad
data[0].is_album
data[0].images[0].type
data[0].images[0].is_ad
data[0].images[0].has_sound
data[0].images[0].mp4
data[0].images[0].gifv

## Extra info from get authorization response
expires_in=315360000
token_type=bearer
account_username=GifReversalBot
account_id=112569647

## File formats I'll have to deal with:
video/mp4
image/gif

less common formats I may want to add?
video/webm
video/x-matroska
video/quicktime
video/x-flv
video/x-msvideo
video/x-ms-wmv
video/mpeg

