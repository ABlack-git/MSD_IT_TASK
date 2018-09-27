package msdhw;

import java.io.File;
import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Scraper {

    private final static Logger LOGGER = Logger.getLogger(Scraper.class.getName());
    private final static List<String> MONTHES
            = Arrays.asList("january", "february", "march", "aril", "may",
                    "june", "july", "august", "september", "october",
                    "november", "december");
    private final static String ROOT_URL = "https://digital.nhs.uk";

    private static String getDataUrls(String url) throws IOException {
        String dataUrl = "";
        try {
            Document doc = Jsoup.connect(url).get();
            Elements elems = doc.select(".attachment");
            for (int i = 0; i < elems.size(); i++) {
                String href = elems.get(i).select("a").attr("href");
                String[] name = new File(href).getName().split("-");
                if (name.length >= 3) {
                    if (name[3].equals("phe")) {
                        dataUrl = href;
                    }
                }

            }
        } catch (IOException e) {
            throw e;
        }

        return dataUrl;
    }

    //private Document doc;
    public static List<String> scrapUrls(String url) throws IOException {
        return Scraper.scrapUrls(url, null);
    }

    public static List<String> scrapUrls(String url, String year) throws IOException {
        List<String> urls = new LinkedList<>();
        Document doc = null;
        try {
            doc = Jsoup.connect(url).get();
        } catch (IOException e) {
            throw e;
        }
        Elements elems = doc.select(".cta");
        for (int i = 0; i < elems.size(); i++) {
            String href = elems.get(i).select("a").attr("href");
            String[] name = new File(href).getName().split("-");
            if (name.length < 2) {
                continue;
            }
            if (MONTHES.contains(name[0])) {
                try {
                    if (year == null) {
                        String dataUrl = getDataUrls(ROOT_URL + href);
                        if (dataUrl.length() == 0) {
                            LOGGER.log(Level.INFO, "Unable to get data URL from "
                                    + ROOT_URL + "{0}", href);
                            continue;
                        }
                        urls.add(dataUrl);
                    } else if (name[1].equals(year)) {
                        String dataUrl = getDataUrls(ROOT_URL + href);
                        if (dataUrl.length() == 0) {
                            LOGGER.log(Level.INFO, "Unable to get data URL from "
                                    + ROOT_URL + "{0}", href);
                            continue;
                        }
                        urls.add(dataUrl);
                    }
                } catch (IOException e) {
                    LOGGER.log(Level.WARNING, e.getMessage(), e);
                }
            }
        }
        return urls;
    }

}
