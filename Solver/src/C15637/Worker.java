package C15637;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.BlockingQueue;

import org.apache.commons.io.IOUtils;

import com.mongodb.DBObject;

public class Worker extends Thread {

	static String ipoptPath = "/home/ubuntu/Ipopt-3.11.9/build/bin/ipopt";
	static String amplPath = "/home/ubuntu/Ipopt-3.11.9/build/bin/ampl";
	// static String ipoptPath =
	// "/home/weiwan/Dropbox/workspace/Ipoptorg/build/bin/ipoptorg";
	// static String amplPath = "/home/weiwan/ampl";

	private final BlockingQueue<String> queue;

	public Worker(BlockingQueue<String> queue) {
		this.queue = queue;
	}

	private File writeCompileFile(String fileName, String modelName)
			throws IOException {

		File file = new File(fileName);

		// if file doesnt exists, then create it
		if (!file.exists()) {
			file.createNewFile();
		}

		FileWriter fw;
		fw = new FileWriter(file.getAbsoluteFile());
		BufferedWriter bw = new BufferedWriter(fw);
		bw.write("model " + modelName + ".mod;\n");
		bw.write("write b" + modelName + ";\n");

		bw.close();

		return file;

	}

	private void doWork(String task) throws IOException {
		Runtime rt = Runtime.getRuntime();

		String idString = task;
		boolean flag = true;
		DBObject submission = utils.MongoDBUtils.getSubmissionbyId(idString);
		if (submission == null) {
			return;
		}
		utils.MongoDBUtils.updateSubmissionStatus(submission, "Running");
		DBObject found = utils.MongoDBUtils.getModelFromSubmission(submission);

		String fileId = found.get("f").toString();
		String fileType = found.get("type").toString();
		String fileName = utils.MongoDBUtils.writeToFile(fileId, fileType,
				found);
		BufferedReader stdInput, stdError;
		String stdOutput, errOutput;
		Process p = null;
		if (fileType.equals(".mod")) {
			String tmpName = fileName + "test.run";
			File f = writeCompileFile(tmpName, fileName);
			p = rt.exec(amplPath + " " + tmpName);
			stdInput = new BufferedReader(new InputStreamReader(
					p.getInputStream()));
			stdError = new BufferedReader(new InputStreamReader(
					p.getErrorStream()));
			try {
				p.waitFor();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			stdOutput = IOUtils.toString(stdInput);
			errOutput = IOUtils.toString(stdError);

			if (p.exitValue() != 0) {
				flag = false;
				utils.MongoDBUtils.updateSubmissionResult(submission,
						stdOutput, errOutput);
			}
			f.delete();
		}

		if (flag) {
			Options options = utils.MongoDBUtils
					.getOptionsFromSubmission(submission);
			options.writeOptionFile();

			String cmd = ipoptPath + " " + fileName + ".nl";
			p = rt.exec(cmd);
			stdInput = new BufferedReader(new InputStreamReader(
					p.getInputStream()));
			stdError = new BufferedReader(new InputStreamReader(
					p.getErrorStream()));
			try {
				p.waitFor();
			} catch (InterruptedException e1) {
				stdInput.close();
				stdError.close();
				e1.printStackTrace();
			}
			stdOutput = IOUtils.toString(stdInput);
			errOutput = IOUtils.toString(stdError);

			utils.MongoDBUtils.updateSubmissionResult(submission, stdOutput,
					errOutput);
			stdInput.close();
			stdError.close();
			File f = new File(fileName + ".nl");
			f.delete();
			System.out.println("Task is done!");
		}
		
		if (!fileType.equals(".nl")) {
			File f = new File(fileName + fileType);
			f.delete();
		}

		if (p.exitValue() == 0) {
			utils.MongoDBUtils.updateSubmissionStatus(submission, "Succeed");
			utils.MongoDBUtils.createNotification(submission, false);
		} else {
			utils.MongoDBUtils.updateSubmissionStatus(submission, "Failed");
			utils.MongoDBUtils.createNotification(submission, true);
		}
	}

	public void run() {
		try {
			while (true) {
				String s = queue.take();
				doWork(s);
			}
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
