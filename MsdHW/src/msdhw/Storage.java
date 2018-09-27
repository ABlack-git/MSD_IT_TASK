package msdhw;

import java.util.List;

public interface Storage {

    public List<String> retriveFiles(List<String> filesToRetrive, String localPath);

    public List<String> storeFiles(String remotePath, List<String> filesToStore);
}
