package C15637;

public class Task {

	
	private String fileName;
	private String idString;
	private String fileType;

	public Task(String fileName, String idString, String fileType) {
		this.fileName = fileName;
		this.idString = idString;
		this.fileType = fileType;
	}

	public String getFileName() {
		return fileName;
	}

	public String getIdString() {
		return idString;
	}
	public String getFileType() {
		return fileType;
	}

	@Override
	public String toString() {
		return "Task [fileName=" + fileName + ", idString=" + idString
				+ ", fileType=" + fileType + "]";
	}


}
