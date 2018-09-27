package msdhw;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.channels.ReadableByteChannel;
import java.nio.channels.Channels;
import java.nio.channels.FileChannel;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class LocalStorage implements Storage {

    private final static Logger LOGGER = Logger.getLogger(LocalStorage.class.getName());

    @Override
    public List<String> storeFiles(String localPath, List<String> urls) {
        List<String> ret = new LinkedList<>();
        new File(localPath).mkdirs();
        for (String url : urls) {
            ReadableByteChannel channel = null;
            FileOutputStream fos = null;
            try {
                channel = Channels.newChannel(new URL(url).openStream());
                String fileName = new File(url).getName();
                String absPath = new File(localPath, fileName).getAbsolutePath();
                fos = new FileOutputStream(absPath);
                FileChannel fChannel = fos.getChannel();
                fChannel.transferFrom(channel, 0, Long.MAX_VALUE);
                LOGGER.log(Level.INFO, "Download complete: {0}", fileName);
                ret.add(absPath);
            } catch (MalformedURLException ex) {
                LOGGER.log(Level.WARNING, ex.getMessage(), ex);
            } catch (IOException ex) {
                LOGGER.log(Level.WARNING, ex.getMessage(), ex);
            } finally {
                try {
                    if (fos != null) {
                        fos.close();
                    }
                    if (channel != null) {
                        channel.close();
                    }
                } catch (IOException ex) {
                    LOGGER.log(Level.WARNING, ex.getMessage(), ex);
                }
            }
        }
        return ret;
    }

    @Override
    public List<String> retriveFiles(List<String> filesToRetrive, String localPath) {
        return filesToRetrive;
    }

}
