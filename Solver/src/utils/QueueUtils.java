package utils;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class QueueUtils {

	private static final BlockingQueue<String> queue = new LinkedBlockingQueue<String>();

	public static BlockingQueue<String> getQueue() {
		return queue;
	}
	

}
