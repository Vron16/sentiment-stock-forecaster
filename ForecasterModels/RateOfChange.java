import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

// Finding the ROC of closing prices of a single stock
public class RateOfChange {
	// ROC interval
	static int NUM_DAYS = 5;
	
	// main
	public static void main(String[] args) { 
		// get fake stock info
		String stock = "GOOGL";
		FakeDatabase db = new FakeDatabase();
		HashMap<String, List<Double>> closingMap = db.getDBs().get(0);
		List<Double> closing = closingMap.get(stock);
		
		// get ROCs
		List<Double> rocs = nDayRateOfChange(NUM_DAYS, closing);
		
		// print info
		db.printList(stock, closing);
		printROC(rocs);
	}
	
	// get ROCs at intervals
	private static List<Double> nDayRateOfChange(int num, List<Double> closing) {
		List<Double> rocs = new ArrayList<>();
		int i = num;
		while (i < closing.size()) {
			rocs.add(calculateROC(closing, i, i-num));
			i+=num;
		}
		return rocs;
	}

	// Calculate ROC
	// ROC = [(Close - Close n periods ago) / (Close n periods ago)] * 100
	private static Double calculateROC(List<Double> closing, int now, int nAgo) {
		double diff = closing.get(now) - closing.get(nAgo);
		double roc = (diff/closing.get(nAgo)) * 100;
		return roc;
	}
	
	// Print ROCs
	private static void printROC(List<Double> rocs) {
		System.out.println("\nROCS");
		for (Double r : rocs) {
			System.out.println(r + "%");
		}
	}

}
