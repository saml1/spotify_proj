# spotify_proj
So far, given a Spotify playlist ID and a local directory containing MP3 files, this program outputs songs that appear in both the Spotify playlist and the local directoy. 

For usage, enter: 
python main.py -h

1.
First, create a config file: 
python3 main.py cc -s1 <YOUR_SPOTIFY_CLIENT_ID> -s2 <YOUR_SPOTIFY_CLIENT_SECRET> -a <YOUR_ACOUSTID_API_KEY> -d <YOUR_DISCOGS_API_TOKEN> -cf ENTER DIRECTORY TO SAVE CONFIG FILE TO>

2.
Once a config file is created, add a Spotify playlist:
python3 main.py ap -db <ENTER FILEPATH OF DATABASE>  -pid <PLAYLIST_ID> -pn <ENTER PLAYLIST NAME>

3.
Then add a local directory:
python3 main.py ad -db <ENTER FILEPATH OF DATABASE> -dir <ENTER DIRECTORY CONTAINING MP3 FILES> -dbn <GIVE NAME FOR SONGS COMING FROM THIS DIRECTORY>

4.
Then to output songs that exist in both the Spotify playlist and local directory:
python3 main.py gd -db <ENTER FILEPATH OF DATABASE> -d1 <SPOTIFY PLAYLIST NAME following -pn in step 2> -d2 <LOCAL SONGS NAME following -dbn in step 3>


Note: for -db command, be sure to end include database file (databasename.db) at end of directory. If the specified database does not exist, one will be created.
EX: /Users/samlipschitz/Documents/spotify_proj/database.db
