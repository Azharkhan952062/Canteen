# Problem Research & Analysis

## 1. The Real-World Problem
**Problem Statement:**
> "The canteen sometimes prepares more Biryani than the actual customer demand. When the demand is lower than expected, unsold Biryani gets spoiled, causing food waste and financial loss. The owner needs a simple way to understand previous demand and make better daily preparation decisions."

**Context & Significance:**
Small campus canteens operate on low profit margins with perishable cooked goods. Unlike packaged items with long shelf lives, cooked rice dishes such as Biryani must be sold on the day of preparation. Preparing too little results in lost sales and customer dissatisfaction, while preparing too much leads to unsold food, spoilage, and direct monetary loss.

---

## 2. Existing Solutions Comparison

### Solution 1: Traditional Manual Paper Ledger
- **Description:** Recording daily counter sales and customer orders in a physical paper register or diary.
- **Advantages:** Zero hardware or software costs; immediately accessible to staff of any technical literacy level.
- **Disadvantages:** Prone to manual calculation errors; cannot automatically aggregate multi-day trends or compute running averages for morning preparation planning.

### Solution 2: Commercial Restaurant Point-of-Sale (POS) Systems
- **Description:** Commercial restaurant inventory systems with digital touchscreens, cloud databases, and automated kitchen displays.
- **Advantages:** Comprehensive real-time tracking of ingredients, inventory deduction, and customer analytics.
- **Disadvantages:** High upfront hardware costs, recurring software subscription fees, and steep learning curves that make them impractical for small campus food stalls.

---

## 3. Academic & Industry Literature
*(Template for student: Record two sources you have genuinely read and consulted for this assignment. Do not invent sources.)*

### Source 1:
- **Title / Author:** 
- **Publication / Date / URL:** 
- **Key Relevance to Problem:** 

### Source 2:
- **Title / Author:** 
- **Publication / Date / URL:** 
- **Key Relevance to Problem:** 

---

## 4. Proposed Lightweight Solution
A local, lightweight Python & Streamlit tool (**Canteen Food Demand & Waste Tracker**) that:
1. Replaces cumbersome paper logs with a simple, transparent CSV structure.
2. Automatically computes remaining quantities ($\text{Prepared} - \text{Sold}$) and overall unsold percentages.
3. Provides visual demand trends and average daily demand benchmarks to guide morning cooking batches.
