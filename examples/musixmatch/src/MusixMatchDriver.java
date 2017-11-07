import org.jmusixmatch.MusixMatch;
import org.jmusixmatch.MusixMatchException;
import org.jmusixmatch.entity.lyrics.Lyrics;
import org.jmusixmatch.entity.track.Track;
import org.jmusixmatch.entity.track.TrackData;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Properties;

public class MusixMatchDriver {


    public static void main(String[] args) throws IOException, MusixMatchException {
        // read parameters
        String trackName = args[0];
        String artistName = args[1];

        // read properties file
        Properties prop = new Properties();
        prop.load(new FileInputStream("config.properties"));

        // Musixmatch API registration
        String apiKey = prop.getProperty("musicmatch_key");
        org.jmusixmatch.MusixMatch musixMatch = new org.jmusixmatch.MusixMatch(apiKey);

        // search musixmatch
        Track track = musixMatch.getMatchingTrack(trackName, artistName);
        TrackData data = track.getTrack();

        System.out.println("AlbumID : "    + data.getAlbumId());
        System.out.println("Album Name : " + data.getAlbumName());
        System.out.println("Artist ID : "  + data.getArtistId());
        System.out.println("Album Name : " + data.getArtistName());
        System.out.println("Track ID : "   + data.getTrackId());

        int trackID = data.getTrackId();
        Lyrics lyrics = musixMatch.getLyrics(trackID);
        System.out.println("Lyrics ID       : "     + lyrics.getLyricsId());
        System.out.println("Lyrics Language : "     + lyrics.getLyricsLang());
        System.out.println("Lyrics Body     : "     + lyrics.getLyricsBody());
        System.out.println("Script-Tracking-URL : " + lyrics.getScriptTrackingURL());
        System.out.println("Pixel-Tracking-URL : "  + lyrics.getPixelTrackingURL());
        System.out.println("Lyrics Copyright : "    + lyrics.getLyricsCopyright());
    }

}
