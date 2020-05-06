import tkinter as tk
import spotipy
import spotipy.util as util

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8888/callback/"
SCOPE = 'playlist-modify-public'

# Create Window
root = tk.Tk()
root.title("Spotify Playlist Copier")
root.geometry("300x100+0+0")


# Input Variables
username = tk.StringVar()
target_name = tk.StringVar()
target_playlist = tk.StringVar()


# Define Buttons/Widgets
user_label = tk.Label(root, text="Enter Username: ").place(x=0, y=0)
user_label = tk.Label(root, text="Enter Target Name: ").place(x=0, y=20)
user_label = tk.Label(root, text="Enter Target Playlist: ").place(x=0, y=40)

user_entry = tk.Entry(root, textvariable=username, width=25).place(x=120, y=0)
user_entry = tk.Entry(root, textvariable=target_name, width=25).place(x=120, y=20)
user_entry = tk.Entry(root, textvariable=target_playlist, width=25).place(x=120, y=40)


def get_tracks(target_id, target_playlist_id, sp):
    results = sp.user_playlist_tracks(target_id, target_playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return list(map(lambda x: x['track']['id'], tracks))

def copy_playlist():
    user_id = username.get()
    target_id = target_name.get()
    target_pl = target_playlist.get()
    print(target_id)

    if user_id == "" or target_id == "" or target_pl == "":
        print("Invalid Entries")

    token = util.prompt_for_user_token(user_id, SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False

        # Check if Target Playlist Exists
        target_playlist_found = False
        target_playlist_id = ""

        target_list = sp.user_playlists(target_id, 50)
        for playlist in target_list['items']:
            if playlist['name'] == target_pl:
                target_playlist_id = playlist['id']
                target_playlist_found = True
                break

        if not target_playlist_found:
            print("Desired Playlist Does Not Exist!")
            return

        # Create A New Playlist For the User
        sp.user_playlist_create(user_id, target_pl, True)
        playlist_id = ""

        user_list = sp.user_playlists(user_id, 50)
        for playlist in user_list['items']:
            if playlist['name'] == target_pl:
                playlist_id = playlist['id']
                break

        track_list = get_tracks(target_id, target_playlist_id, sp)
        sp.user_playlist_add_tracks(user_id, playlist_id, track_list)
    else:
        print("Token not received.")


copy = tk.Button(root, text="copy playlist", command=copy_playlist).place(x=110, y=70)

root.mainloop()


