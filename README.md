This Python project creates a Spotify playlist of the top 100 songs from a specific date, based on the Billboard Hot 100. 
It scrapes song titles from the Billboard website for a user-specified date, then uses the Spotify API to search for those songs and add them to a new Spotify playlist.

Technologies Used:
Python
BeautifulSoup (for web scraping)
Spotify API (via the Spotipy library)
Requests
dotenv (for securely storing sensitive information)

Setup Instructions:
Clone this repository to your local machine
Install the required dependencies
Create a .env file and add your Spotify API credentials
(CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://localhost:8888/callback
USERNAME=your_spotify_username)
