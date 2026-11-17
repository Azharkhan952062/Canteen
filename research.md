# Problem Research & Analysis

## 1. Problem Identification
1. The campus canteen experiences daily demand fluctuations for its primary cooked menu items, especially Biryani.
2. In the morning, kitchen staff prepare fixed batches of food based on intuition rather than historical demand data.
3. On days with lower student footfall, substantial portions of cooked Biryani remain unsold at the close of operations.
4. Because cooked Biryani is perishable and cannot be carried over indefinitely, unsold portions risk rapid spoilage.
5. This recurring over-preparation directly causes avoidable food waste and direct financial losses for the canteen operator.

---

## 2. Existing Solutions and Their Limitations for Small Canteens

### Solution 1: Physical Paper Ledgers and Registers
- **Operational Mechanism:** The counter staff writes orders, cash collected, and daily notes inside a paper notebook or spiral diary at the counter.
- **Why It Does Not Fully Suit This Canteen:** While paper ledgers have zero software cost and are easy to write in during busy hours, they keep sales data trapped in static rows. Counter staff cannot quickly compute running averages, calculate unsold food rates across days, or visualize sales trends to guide next-morning preparation quantities.

### Solution 2: Enterprise Restaurant Point-of-Sale (POS) Systems
- **Operational Mechanism:** Commercial digital restaurant software suites running on dedicated POS terminals with barcode scanners, cloud synchronization, and automated inventory reconciliation.
- **Why It Does Not Fully Suit This Canteen:** Commercial POS systems demand significant upfront hardware investments, ongoing monthly software subscription fees, and complex catalog setups. For a small campus canteen with a focused menu (such as Biryani and Chicken Roll) and single-counter service, these systems introduce excessive complexity and overhead without providing a straightforward daily cooking recommendation.

---

## 3. Credible Industry and Academic Literature

### Source 1: Food Waste Index Report 2024
- **Title & Organization:** *Food Waste Index Report 2024: Think Eat Save - Tracking Global Food Waste*, United Nations Environment Programme (UNEP) and WRAP.
- **Publication Details & URL:** UNEP, Nairobi, March 2024. https://www.unep.org/resources/publication/food-waste-index-report-2024
- **Summary:**
  The report evaluates global food waste, documenting that approximately 1.05 billion tonnes of food were discarded in 2022, with the food service and hospitality sector accounting for 28 percent (290 million tonnes). It highlights that over-preparation in institutional kitchens and small food establishments represents a major contributor to avoidable food disposal. The authors emphasize that regular kitchen-level tracking and routine measurement are critical upstream interventions to prevent waste before food is cooked.
- **Relevance to This Project:**
  This report provides authoritative evidence that food service over-preparation is a significant operational challenge. It reinforces the core objective of our application: enabling small food operators to track daily consumption patterns so kitchen preparation directly aligns with actual demand.

### Source 2: The State of Food and Agriculture 2019
- **Title & Organization:** *The State of Food and Agriculture 2019: Moving forward on food loss and waste reduction (SOFA 2019)*, Food and Agriculture Organization of the United Nations (FAO).
- **Publication Details & URL:** FAO, Rome, 2019. ISBN: 978-92-5-131789-1. https://www.fao.org/state-of-food-agriculture/2019/en/
- **Summary:**
  This flagship FAO report examines the economic, environmental, and operational causes of food loss and waste across global food chains. It demonstrates that food business operators have strong financial incentives to curb waste, as discarded food directly erodes operating profit margins. The report concludes that identifying critical loss points and adopting localized data tracking allows small and medium food enterprises to balance supply with demand cost-effectively.
- **Relevance to This Project:**
  This study substantiates the economic rationale of our project. It confirms that helping small canteen operators quantify unsold portions and monitor daily sales provides direct financial protection while mitigating food waste.

---

## 4. Scope and Positioning of the Canteen Tracker
The **Canteen Food Demand & Waste Tracker** fills the gap between static paper diaries and expensive enterprise software. By reading a lightweight, transparent CSV file (`data.csv`), the tool automatically calculates remaining quantities ($\text{Quantity\_Remaining} = \text{Quantity\_Prepared} - \text{Quantity\_Sold}$), visualizes historical sales patterns, and provides average demand guidance for daily morning preparation.
