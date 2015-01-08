package C15637;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class Options {
	private String linear_solver;
	private double tol;
	private int maxIter;
	private double bound_frac;
	private double bound_push;
	public Options(String linear_solver, double tol, int maxIter,
			double bound_frac, double bound_push) {
		this.linear_solver = linear_solver;
		this.tol = tol;
		this.maxIter = maxIter;
		this.bound_frac = bound_frac;
		this.bound_push = bound_push;
	}
	public void writeOptionFile() throws IOException{
		File file = new File("ipopt.opt");

		// if file doesnt exists, then create it
		if (!file.exists()) {
			file.createNewFile();
		}

		FileWriter fw;
		fw = new FileWriter(file.getAbsoluteFile());
		BufferedWriter bw = new BufferedWriter(fw);
		bw.write("linear_solver " + linear_solver + "\n");
		bw.write("tol " + tol + "\n");
		bw.write("max_iter " + maxIter + "\n");
		bw.write("bound_frac " + bound_frac + "\n");
		bw.write("bound_push " + bound_push + "\n");
		bw.close();
	}
	
}
