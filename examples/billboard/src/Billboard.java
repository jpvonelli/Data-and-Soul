import com.google.gson.Gson;
import org.apache.http.*;
import org.apache.http.client.*;
import org.apache.http.client.methods.*;
import org.apache.http.impl.client.*;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.*;

public class Billboard {

    static final String CHARTS_ENDPOINT_URL = "http://billboard.modulo.site/charts/";
    private HttpClient httpClient;

    Billboard() {
        this.httpClient = HttpClientBuilder.create().build();
    }

    Song[] getChart(final Date date, int max) throws IOException {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        String dateStr = dateFormat.format(date);
        System.out.println(dateStr);
        HttpGet request = new HttpGet(Billboard.CHARTS_ENDPOINT_URL + dateStr + "?filter=song&max=" + max);
        request.setHeader(HttpHeaders.CONTENT_TYPE, "application/json");
        HttpResponse response = this.httpClient.execute(request);
        System.out.println("Response Code : " + response.getStatusLine().getStatusCode());
        String responseString = new BasicResponseHandler().handleResponse(response);
        return new Gson().fromJson(responseString, Song[].class);
    }

    public static void main(String[] args) throws IOException {
        Calendar cal = Calendar.getInstance();
        cal.set(1972, 5, 3);
        Date date = cal.getTime();
        Song[] chart = new Billboard().getChart(date, 10);
        System.out.println(Arrays.toString(chart));
    }
}