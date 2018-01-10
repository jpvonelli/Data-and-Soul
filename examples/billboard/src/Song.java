public class Song {

    public String rank, song_id, song_name, artist_id, display_artist, spotify_id;

    @Override
    public String toString() {
        return "{rank: " + rank + ", song_id: " + song_id + ", song_name: " + song_name + ", artist_id: " + artist_id + ", display_artist: " + display_artist + ", spotify_id: " + spotify_id + "}";
    }
}
