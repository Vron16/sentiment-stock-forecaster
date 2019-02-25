import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

// Finding the likelihood to switch directions (volatility)
public class StochasticOscillator {
	// SO interval
	static int NUM_DAYS = 10;
	
	// main
	public static void main(String[] args) { 
		// get fake stock info
		String stock = "GOOGL";
		FakeDatabase db = new FakeDatabase();
		
		// get dbs and list
		HashMap<String, List<Double>> closingMap = db.getDBs().get(0);
		HashMap<String, List<Double>> highMap = db.getDBs().get(1);
		HashMap<String, List<Double>> lowMap = db.getDBs().get(2);
		HashMap<String, List<Double>> curMap = db.getDBs().get(3);
		List<Double> close = closingMap.get(stock);
		List<Double> high = highMap.get(stock);
		List<Double> low = lowMap.get(stock);
		List<Double> cur = curMap.get(stock);
		
		// get oscillation percentage
		List<Double> sos = nDayOscillation(NUM_DAYS, close, high, low, cur);
		
		// print info
		db.printList(stock, cur);
		printSOs(sos);
	}
	
	// get oscillation percentage
	private static List<Double> nDayOscillation(int num, List<Double> close, List<Double> high, List<Double> low,
			List<Double> cur) {
		List<Double> sos = new ArrayList<>();
		int dbSize = close.size(); // assuming all the same size
		int i = num;
		while (i < dbSize) {
			sos.add(calculateSO(close, high, low, cur, i, i-num));
			i+=num;
		}
		return sos;
	}

	// Calculate SO
	// SO = [(Current - Lowest in n periods) / (High in n periods - Lowest in n periods)] * 100
	private static Double calculateSO(List<Double> close, List<Double> high, List<Double> low, List<Double> cur, int now, int nAgo) {
		// initialize
		double curPrice = cur.get(now);
		double highPrice = 0;
		double lowPrice = Double.MAX_VALUE;
		
		// find lowest and highest of the n day period
		int i = nAgo;
		while (i <= now) {
			if (high.get(i) > highPrice) {
				highPrice = high.get(i);
			}
			
			if (low.get(i) < lowPrice) {
				lowPrice = low.get(i);
			}
			i++;
		}
		
		// calculate
		double numer = curPrice - lowPrice;
		double denom = highPrice-lowPrice;
		double percent = (numer/denom) * 100;
		return percent;
	}
	
	// Print SOs
	private static void printSOs(List<Double> sos) {
		System.out.println("\nSOs");
		for (Double r : sos) {
			System.out.println(r + "%");
		}
	}

}
