# spotify_proj
So far, given a Spotify playlist ID and a local directory containing MP3 files, this program outputs songs that appear in both the Spotify playlist and the local directoy. 

It currently only searches for perfect matches, i.e., length (+- 10 seconds) and metadata of the local MP3 is idential to song info obtained from Spotify's API.

A more precise matching algorithm that does not rely on identical metadata is in the works!

For usage, enter: 
`python main.py -h`

1.
First, create a config file: 
`python3 main.py cc -s1 <YOUR_SPOTIFY_CLIENT_ID> -s2 <YOUR_SPOTIFY_CLIENT_SECRET> -a <YOUR_ACOUSTID_API_KEY> -d <YOUR_DISCOGS_API_TOKEN>`

2.
Once a config file is created, add a Spotify playlist:
`python3 main.py ap -pid <PLAYLIST_ID> -ln <ENTER PLAYLIST NAME>`

3.
Then add a local directory:
`python3 main.py ad -dir <ENTER DIRECTORY CONTAINING MP3 FILES> -ln <GIVE NAME FOR SONGS COMING FROM THIS DIRECTORY>`

4.
Then to output songs that exist in both the Spotify playlist and local directory:
`python3 main.py gd -d1 <SPOTIFY PLAYLIST NAME following -ln in step 2> -d2 <LOCAL SONGS NAME following -ln in step 3>`