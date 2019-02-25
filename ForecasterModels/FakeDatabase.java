import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Temporary database- TODO: replace with DB connector to real database
public class FakeDatabase {
	List<HashMap<String, List<Double>>> dbs;
	HashMap<String, List<Double>> closingPriceDB;
	HashMap<String, List<Double>> highPriceDB;
	HashMap<String, List<Double>> lowPriceDB;
	HashMap<String, List<Double>> curPriceDB;
	
	// constructor
	public FakeDatabase() {
		closingPriceDB = new HashMap<>();
		highPriceDB = new HashMap<>();
		lowPriceDB = new HashMap<>();
		curPriceDB = new HashMap<>();
		dbs = new ArrayList<HashMap<String, List<Double>>>();
		dbs.add(closingPriceDB);
		dbs.add(highPriceDB);
		dbs.add(lowPriceDB);
		dbs.add(curPriceDB);
		loadDBs();
	}
	
	// randomly generate values for databases
	private void loadDBs() {
		List<Double> close = new ArrayList<Double>();
		List<Double> high = new ArrayList<Double>();
		List<Double> low = new ArrayList<Double>();
		List<Double> cur = new ArrayList<Double>();
		for (int i = 1; i <= RateOfChange.NUM_DAYS*2; i++) {
			for (int j = 1; j <= RateOfChange.NUM_DAYS; j++) {
				double p = Math.abs(Math.random()+10*(j/i)*Math.random())+2;
				close.add(p);
				high.add(p+2);
				low.add(Math.abs(p-2));
				cur.add(p-1);
			}
		}
		closingPriceDB.put("GOOGL", close);
		highPriceDB.put("GOOGL", high);
		lowPriceDB.put("GOOGL", low);
		curPriceDB.put("GOOGL", cur);
	}
	
	// print closing prices as a horizontal bar graph
	public void printList(String stock, List<Double> list) {
		System.out.println("Stock prices of: " + stock);
		int num = 0;
		for (Double price : list) {
			int i = 0;
			System.out.print(num + ": ");
			while (i < price) {
				System.out.print("x");
				i++;
			}
			System.out.println();
			num++;
		}
	}
	
	// get database
	public List<HashMap<String, List<Double>>> getDBs() {
		return dbs;
	}
	
}
