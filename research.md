# Problem Research & Analysis

## 1. The Real-World Problem
**Problem Statement:**
> "The canteen sometimes prepares more Biryani than the actual customer demand. When the demand is lower than expected, unsold Biryani gets spoiled, causing food waste and financial loss. The owner needs a simple way to understand previous demand and make better daily preparation decisions."

**Operational Context:**
Small campus canteens operate with high perishability and tight margins. Cooked items like Biryani cannot be preserved overnight without significant flavor loss and food safety concerns. When the kitchen over-prepares, the unsold portions directly turn into food wastage and financial loss. When the kitchen under-prepares, the canteen loses potential revenue and customer satisfaction.

---

## 2. Existing Solutions and Their Limitations

### Existing Approach 1: Manual Paper Ledgers
- **Mechanism:** Recording customer orders, cash received, and daily item preparation in physical notebooks.
- **Strengths:** Zero technology cost; immediately usable by any counter staff.
- **Limitations:** Data remains siloed in handwritten pages; difficult to aggregate historical totals, compute daily averages, or visualize multi-day trends for future morning preparation planning.

### Existing Approach 2: Enterprise Restaurant POS & Inventory Systems
- **Mechanism:** Commercial cloud-based POS software with barcode scanning, dedicated touch terminals, and automated kitchen display systems.
- **Strengths:** Real-time stock alerts, deep analytics, and multi-terminal sync.
- **Limitations:** High initial hardware costs, recurring software subscriptions, and excessive feature complexity that make them unfeasible and burdensome for small, single-counter campus food stalls.

---

## 3. Scope of the Proposed Lightweight Solution
The **Canteen Food Demand & Waste Tracker** addresses this specific operational gap by providing:
1. A straightforward, transparent data store based on standard CSV records.
2. Automated calculation of remaining stock ($\text{Quantity\_Remaining} = \text{Quantity\_Prepared} - \text{Quantity\_Sold}$).
3. Visual demand comparison across menu items (Biryani Half, Biryani Full, Chicken Roll).
4. Daily preparation guidance based on historical average sales to help counter staff make informed morning batch decisions.
