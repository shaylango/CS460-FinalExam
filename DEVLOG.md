# Development Log – The Torchbearer

**Student Name:** Shayla Ngo
**Student ID:** 828275819

---

## Entry 1 – [5/11/26]: Initial Plan

Before writing any code, I think my plan is that I will first implement explain_problem(), and just go in that order. The part I expect to be difficult is probably part 5, which is the state and search space since I have to correctly track multiple variables while also exploring a large search space. Lastly, I plan to test using the provided tests.

---

## Entry 2 – [5/13/26]: Design Change

While I was testing, I realized that a set can't maintain the exact sequence of relics visited. So I fixed it by using a set for faster checks and a list to record the exact order. 

---

## Entry 3 – [5/14/26]: Bug Fix

After testing, I realized my search loop was trying to remove elements from relics_remaining, while also iterating over that same set. I fixed this by iterating over a list copy of the set instead.

---

## Entry 4 – [5/14/26]: Post-Implementation Reflection

After my implementation, I would say that I wouldn't really change anything, and everything works pretty well. However, given more time I could possibly improve the pruning strategy and add more edge case tests.

---

## Final Entry – [5/14/26]: Time Estimate

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 40 min |
| Part 2: Precomputation Design | 2 hours |
| Part 3: Algorithm Correctness | 1 hour |
| Part 4: Search Design | 1 hour |
| Part 5: State and Search Space | 1 hour |
| Part 6: Pruning |  2 hours |
| Part 7: Implementation | 3 hours |
| README and DEVLOG writing | 4 hours |
| **Total** | 15 hours |
