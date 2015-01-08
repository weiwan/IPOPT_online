package C15637;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.concurrent.BlockingQueue;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


import com.mongodb.MongoException;

/**
 * Servlet implementation class q1
 */
@WebServlet("/q2")
public final class q2 extends HttpServlet {
	private static final long serialVersionUID = 1L;
	static String s = null;
	private static final int POOL_SIZE = 1;
	private static BlockingQueue<String> queue;

	/**
	 * @see HttpServlet#HttpServlet()
	 */
	public q2() {
		super();
		// TODO Auto-generated constructor stub
	}

	/**
	 * @see Servlet#init(ServletConfig)
	 */
	public void init(ServletConfig config) throws ServletException {
		// TODO Auto-generated method stub
		queue = utils.QueueUtils.getQueue();
		try {
			utils.MongoDBUtils.connect();
		} catch (MongoException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		for (int i = 0; i < POOL_SIZE; i++) {
			Worker worker = new Worker(queue);
			worker.start();
		}
	}

	/**
	 * @see Servlet#destroy()
	 */
	public void destroy() {
		// TODO Auto-generated method stub
		utils.MongoDBUtils.destory();
	}

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doGet(HttpServletRequest request,
			HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		System.out.print("Start\n");
		response.setContentType("application/json");
		response.setCharacterEncoding("UTF-8");
		PrintWriter responseOut = response.getWriter();
		String idString = request.getParameter("id");
		if(idString == null || idString.equals("")){
			return;
		}

		
		try {
			queue.put(idString);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		responseOut.write("submission succeed!");
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doPost(HttpServletRequest request,
			HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
	}

}