package msdhw;

import java.io.IOException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Main {

    private final static Logger LOGGER = Logger.getLogger(Main.class.getName());

    public static void initLogger() {
        Logger log = Logger.getLogger("");
        log.setLevel(Level.INFO);
    }

    public static void storeToLocalAndFTP() {
        //url that specifies where to start scraping
        String url = "https://digital.nhs.uk/data-and-information/publications"
                + "/statistical/recorded-dementia-diagnoses";
        //year for which to download files
        String date = "2017";
        //public ftp server
        String hostname = "ftp.dlptest.com";
        String username = "dlpuser@dlptest.com";
        String password = "e73jzTRTNqCN9PYAAjjn";
        String localDir = "tmp/";
        String remoteDir = "nhs/dem_geographical";
        try {
            List<String> data = Scraper.scrapUrls(url, date);
            LocalStorage local = new LocalStorage();
            data = local.storeFiles(localDir, data);
            FTPStorage ftp = new FTPStorage(hostname, username, password);
            ftp.storeFiles(remoteDir, data);
        } catch (IOException e) {
            LOGGER.log(Level.SEVERE, e.getMessage(), e);
            System.exit(1);
        }
    }

    public static void main(String[] args) {
        initLogger();
        storeToLocalAndFTP();
    }

}
