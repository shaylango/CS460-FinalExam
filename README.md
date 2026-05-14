# The Torchbearer

**Student Name:** Shayla Ngo
**Student ID:** 828275819
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  A single shortest-path run from S is not enough because it'll only find the min distance to each node, but not the best order for visiting multiple relics.

- **What decision remains after all inter-location costs are known:**
  The decision that remains after all inter-location costs are known is the best order for visiting all the relics.

- **Why this requires a search over orders (one sentence):**
  This requires a search over orders because there are different costs depending on the order of relics.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Spawn | To find the distance from the spawn to the rest of the relics |
| Relics | To find the distance between other relics and the exit |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested Dictionary |
| What the keys represent | Outer keys are starting nodes and inner keys are destination nodes |
| What the values represent | Min distance between nodes |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Dictionaries use hash tables in constant time to get values |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** k + 1
- **Cost per run:** O(mlogn)
- **Total complexity:** O((k + 1) mlogn)
- **Justification (one line):** Runs once from spawn and once from each relic.

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  The stored distance is the optimal shortest path from the source.

- **For nodes not yet finalized (not in S):**
  The distance is the shortest path that is known so far, which only uses the finalized nodes along the path. 

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
  The distance of the source is 0 and all the others are infinity, which there are no wrong distances at the start. 

- **Maintenance : why finalizing the min-dist node is always correct:**
  Having nonnegative edge weights means that no shorter path could be found through an unvisited node. 

- **Termination : what the invariant guarantees when the algorithm ends:**
  All nodes that are finalized have the optimal shortest path from the source.

### Part 3c: Why This Matters for the Route Planner
Correct distances make sure that the route planner chooses the min cost path.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** Greedy picks the closest next relic without considering the cost of the route.
- **Counter-example setup:** Using the spec, the B is closest from S, and greedy would continue choosing relics in that order until reaching the exit.
- **What greedy picks:** S -> B -> C -> D -> T, total cost 301
- **What optimal picks:** S -> B -> D -> C -> T, total cost of 4
- **Why greedy loses:** Choosing the closest next relic does not always result in having a lower total cost. 

### What the Algorithm Must Explore
- The algorithm must explore every possible order in which the relics can be visited to find the min total cost. 

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | node | Location of the node's current path |
| Relics already collected | relics_remaining | set | Set of relics that still need to be visited |
| Fuel cost so far | cost_so_far | int | Total cost of the fuel used so far along the path |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | Set |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | A set allows the operations to run at constant time, which is faster for backtracking |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k!
- **Why:** Every possible sequence of visits might have to be evaluated.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** The min total cost that is found so far and the order of relics for that path. 
- **When it is used:** Used before continuing recursive branch in _explore()
- **What it allows the algorithm to skip:** Any path that is greater than or equal to the min cost found so far. 

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** The total fuel cost, current location, and remaining relics.
- **What the lower bound accounts for:** Accounts for the current cost so far as the min possible cost for that path.
- **Why it never overestimates:** Ignores any potential future cost.

### Part 6c: Pruning Correctness

- Pruning is safe because the cost will increase for any further steps, which means it can't be optimal.

---

## References

- https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/ , For Dijkstra's Algorithm
