package msdhw;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPReply;
import org.apache.commons.net.ftp.FTP;

public class FTPStorage implements Storage {

    private final static Logger LOGGER = Logger.getLogger(FTPStorage.class.getName());

    private final FTPClient client;
    private final String hostname;
    private final String password;
    private final String username;

    public FTPStorage(String hostname, String username, String password) {
        this.client = new FTPClient();
        this.hostname = hostname;
        this.username = username;
        this.password = password;
    }

    private void makeDirs(String path) throws IOException {
        String[] splitedPath = path.split("/");
        if (splitedPath.length > 0) {
            for (String pathElemnt : splitedPath) {
                boolean success = client.changeWorkingDirectory(pathElemnt);
                if (!success) {
                    boolean created = client.makeDirectory(pathElemnt);
                    if (created) {
                        LOGGER.log(Level.INFO, "Directory {0} was created on ftp server.", pathElemnt);
                        client.changeWorkingDirectory(pathElemnt);
                    } else {
                        LOGGER.log(Level.WARNING, "Unable to create directory "
                                + "{0} on ftp server. FTP Reply {1}",
                                new String[]{pathElemnt, client.getReplyString()});
                    }
                }
            }
        }
        client.changeWorkingDirectory("/");
    }

    private boolean connectAndLogin() {
        boolean login = false;
        try {
            client.connect(hostname);
            int reply = client.getReplyCode();
            if (!FTPReply.isPositiveCompletion(reply)) {
                client.disconnect();
                LOGGER.log(Level.WARNING, "Unable to connect. {0}", client.getReplyString());
                return false;
            }
            login = client.login(username, password);
            if (!login) {
                LOGGER.log(Level.WARNING, "Unable to log in. {0}", client.getReplyString());
            }
        } catch (IOException ex) {
            if (client.isConnected()) {
                try {
                    client.disconnect();
                } catch (IOException e) {
                    LOGGER.log(Level.SEVERE, e.getMessage(), e);
                }
            }
            LOGGER.log(Level.SEVERE, ex.getMessage(), ex);
        }
        return login;
    }

    private void disconnectAndLogout(boolean login) {
        if (login) {
            try {
                client.logout();
            } catch (IOException ex) {
                LOGGER.log(Level.SEVERE, ex.getMessage(), ex);
            }
        }
        if (client.isConnected()) {
            try {
                client.disconnect();
            } catch (IOException ex) {
                LOGGER.log(Level.SEVERE, ex.getMessage(), ex);
            }
        }
        LOGGER.log(Level.FINE, "Loged out and disconnected");
    }

    @Override
    public List<String> storeFiles(String remotePath, List<String> filesToStore) {
        List<String> ret = new LinkedList<>();
        if (filesToStore.isEmpty()) {
            return ret;
        }
        boolean login = connectAndLogin();
        if (!login) {
            disconnectAndLogout(login);
            return ret;
        }
        try {
            makeDirs(remotePath);
        } catch (IOException ex) {
            LOGGER.log(Level.SEVERE, ex.getMessage(), ex);
            return ret;
        }
        for (String filePath : filesToStore) {
            FileInputStream fis = null;
            try {
                fis = new FileInputStream(filePath);
                String fileName = new File(filePath).getName();
                String absPath = new File(remotePath, fileName).getPath();
                client.enterLocalPassiveMode();
                client.setFileType(FTP.BINARY_FILE_TYPE);
                boolean success = client.storeFile(absPath, fis);
                if (!success) {
                    LOGGER.log(Level.WARNING, "Unable to upload {0}. Server "
                            + "reply: {1}", new String[]{absPath, client.getReplyString()});
                } else {
                    LOGGER.log(Level.INFO, "Upload complete: {0}", fileName);
                    ret.add(absPath);
                }
            } catch (IOException e) {
                LOGGER.log(Level.WARNING, e.getMessage(), e);
            } finally {
                if (fis != null) {
                    try {
                        fis.close();
                    } catch (IOException e) {
                        LOGGER.log(Level.WARNING, e.getMessage(), e);
                    }
                }
            }
        }
        disconnectAndLogout(login);
        return ret;
    }

    @Override
    public List<String> retriveFiles(List<String> filesToRetrive, String localPath) {
        List<String> ret = new LinkedList<>();
        if (filesToRetrive.isEmpty()) {
            return ret;
        }
        new File(localPath).mkdirs();
        boolean login = connectAndLogin();
        if (!login) {
            disconnectAndLogout(login);
            return ret;
        }

        for (String file : filesToRetrive) {
            String fileName = new File(file).getName();
            File f = new File(localPath, fileName);
            OutputStream os = null;
            try {
                os = new BufferedOutputStream(new FileOutputStream(f));
                client.enterLocalPassiveMode();
                client.setFileType(FTP.BINARY_FILE_TYPE);
                boolean success = client.retrieveFile(file, os);
                if (success) {
                    LOGGER.log(Level.INFO, "Download complete: {0}", fileName);
                    ret.add(f.getAbsolutePath());
                } else {
                    LOGGER.log(Level.WARNING, "Unable to download file: {0}", file);
                }
            } catch (IOException e) {
                LOGGER.log(Level.WARNING, e.getMessage(), e);
            } finally {
                if (os != null) {
                    try {
                        os.close();
                    } catch (IOException ex) {
                        LOGGER.log(Level.SEVERE, ex.getMessage(), ex);
                    }
                }
            }
        }
        disconnectAndLogout(login);
        return ret;
    }

}
