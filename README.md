# Notes
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