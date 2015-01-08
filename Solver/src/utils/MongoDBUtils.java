package utils;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.UnknownHostException;
import java.util.Arrays;
import java.util.Calendar;

import org.bson.types.ObjectId;

import C15637.AnalyseResults;
import C15637.Options;

import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import com.mongodb.MongoCredential;
import com.mongodb.MongoException;
import com.mongodb.ServerAddress;
import com.mongodb.gridfs.GridFS;
import com.mongodb.gridfs.GridFSDBFile;

public class MongoDBUtils {
	private static MongoClient mongoClient = null;
	private static DB db = null;
	private static DBCollection submissionColl = null;
	private static DBCollection modelColl = null;
	private static DBCollection resultColl = null;
	private static DBCollection optionColl = null;
	private static DBCollection notificationColl = null;
	private static DBCollection userColl = null;
	private static GridFS gridfs = null;

	public MongoDBUtils() {
		// TODO Auto-generated constructor stub
	}

	public static DB connect() {
		try {
			MongoCredential credential = MongoCredential
					.createMongoCRCredential("weiwan", "IPOPT",
							"8962269".toCharArray());

			mongoClient = new MongoClient(new ServerAddress("107.21.222.181"),
					Arrays.asList(credential));
			db = mongoClient.getDB("IPOPT");
			gridfs = new GridFS(db);
			submissionColl = db.getCollection("submission");
			modelColl = db.getCollection("n_l_p_model");
			resultColl = db.getCollection("result");
			optionColl = db.getCollection("option");
			notificationColl = db.getCollection("notification");
			userColl = db.getCollection("user");
			// System.out.println("Connected");
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (MongoException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return db;
	}

	public static void destory() {
		if (mongoClient != null) {
			try {
				mongoClient.close();
			} catch (MongoException e) {
				e.printStackTrace();
			}
		}
	}

	public static DBObject getSubmissionbyId(String id) {
		DBObject submission = null;
		try {
			DBObject searchById = new BasicDBObject("_id", new ObjectId(id));
			submission = submissionColl.findOne(searchById);
		} catch (MongoException e) {
			e.printStackTrace();
		}
		return submission;
	}

	public static DBObject getModelFromSubmission(DBObject submission) {
		return modelColl.findOne(submission.get("model"));
	}

	public static Options getOptionsFromSubmission(DBObject submission) {
		Options options = null;

		DBObject found = optionColl.findOne(submission.get("option"));
		options = new Options((String) found.get("linear_solve"),
				(Double) found.get("tol"), (Integer) found.get("max_iter"),
				(Double) found.get("bound_frac"),
				(Double) found.get("bound_push"));

		return options;
	}

	public static void updateSubmissionStatus(DBObject submission, String status) {

		submission.put("status", status);

		Calendar calobj = Calendar.getInstance();
		submission.put("start_time", calobj.getTime());
		submissionColl.save(submission);

	}

	public static void updateSubmissionResult(DBObject submission,
			String stdOutput, String errOutput)
			throws UnsupportedEncodingException {
		AnalyseResults analyseResults = new AnalyseResults(stdOutput);
		BasicDBObject result = new BasicDBObject("std", stdOutput)
				.append("err", errOutput).append("code", 0)
				.append("objective", analyseResults.getObjective())
				.append("exit_tag", analyseResults.getExitTag())
				.append("iters", analyseResults.getIters());
		resultColl.insert(result);
		ObjectId resultId = (ObjectId) result.get("_id");

		submission.put("result", resultId);
		submissionColl.save(submission);

		DBObject model = modelColl.findOne(submission.get("model"));
		model.put("m", analyseResults.getM());
		model.put("n", analyseResults.getN());
		model.put("mineq", analyseResults.getMineq());
		model.put("meq", analyseResults.getMeq());
		modelColl.save(model);

		if ((Boolean) submission.get("sendemail")) {
			utils.EmailUtils.sendResult((String) submission.get("email"),
					stdOutput);
		}

	}

	public static void createNotification(DBObject submission, boolean error) {
		String title;
		if (error) {
			title = "Your submission " + submission.get("title")
					+ " encountered an error!";
		} else {
			title = "Your submission " + submission.get("title") + " is done!";
		}
		Calendar calobj = Calendar.getInstance();
		BasicDBObject notification = new BasicDBObject("user",
				submission.get("user"))
				.append("read", false)
				.append("title", title)
				.append("time", calobj.getTime())
				.append("url",
						"/getresultfile/" + submission.get("result").toString());
		notificationColl.insert(notification);

	}

	public static String writeToFile(String fileId, String type, DBObject found) {
		GridFSDBFile file = gridfs.findOne((ObjectId) found.get("f"));
		String fileName = "/tmp/" + fileId;
		try {
			file.writeTo(fileName + type);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return fileName;
	}
}
