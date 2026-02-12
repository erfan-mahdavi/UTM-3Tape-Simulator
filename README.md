# UTM-3Tape-Simulator
An implementation of the 3-Tape Universal Turing Machine described in "Theory of Computation" course materials.

# 3-Tape Universal Turing Machine (UTM) Simulator

A faithful implementation of the Universal Turing Machine architecture described in the *Theory of Computation* course. This project visualizes how a single fixed machine (the UTM) can simulate any other Turing Machine by reading its description from a dedicated tape.


---

## 🏗 Architecture

This simulator implements the **3-Tape Structure** defined in the course presentation (Slides 28-30):

1. **Tape 1 (Description of M):** Read-Only. Stores the binary encoding of the target machine's transition rules (e.g., `10110...`).
2. **Tape 2 (Contents of M):** Read/Write. Acts as the working memory for the simulated machine, holding the input string.
3. **Tape 3 (State of M):** Read/Write. Stores the current internal state of the simulated machine (e.g., `q1`).

## 🔢 Encoding Standard

The simulator uses the exact Unary/Binary encoding described in **Slide 25** and **Slide 38**:

* **States:** `q1` → `1`, `q2` → `11`, `q3` → `111`...
* **Symbols:** `_` (Blank) → `1`, `1` → `11`, `0` → `111`...
* **Directions:** `R` → `1`, `L` → `11`
* **Separators:** `0` separates elements within a rule, `00` separates distinct rules.

### Example Encoding (from Slide 38)

Rule: *If in state q1, read 1 -> write 1, move Right, stay in q1.*

* **JSON:** `{"q": "q1", "read": "1", "next_q": "q1", "write": "1", "move": "R"}`
* **Binary:** `1 0 11 0 1 0 11 0 1`

---

## 🚀 How to Run

### Prerequisite

You need **Python 3** installed. No external libraries are required.

### 1. Setup

Ensure your folder structure looks like this:

```
UTM-Simulator/
├── main.py
├── src/
│   ├── compiler.py
│   └── utm.py
└── examples/
    └── increment.json
```

### 2. Run the "Unary Increment" Example

This example (from Slide 38) reads a string of 1s (e.g., `111`), moves to the end, and adds a `1`.

```bash
python main.py examples/increment.json 111
```

### 3. Output Explanation

The output shows the state of all 3 tapes at every step of the simulation:

```
[Step 1]
Tape 1 (Desc): 101101010100101011... (The binary rules of M)
Tape 2 (Work): [1] 1 1               (The head is reading the first '1')
Tape 3 (Stat): [q1] (Binary: 1)      (Current state is q1)
```

---

## 📂 Project Structure

### `src/compiler.py`

Translates human-readable JSON rules into the formal `0` and `1` string required for Tape 1. It strictly follows the mapping:

* $q_i \to 1^i$
* $a_j \to 1^j$
* Separator $\to 0$

### `src/utm.py`

The simulation engine. It implements the "Cycle of Operation" (Slide 30):

1. Read current state from Tape 3 and current symbol from Tape 2.
2. Scan Tape 1 to find a matching transition rule.
3. Execute the rule: update Tape 2 (write/move) and Tape 3 (new state).

### `examples/increment.json`

A JSON representation of the "Unary Increment" machine used in the course slides.

---

## 📚 Theory Reference

* **Universality:** The project demonstrates that a single UTM can execute any algorithm if provided with the correct description number.
* **The Halting Problem:** Since TMs can be encoded as strings (Tape 1), we can enumerate them, leading to proofs about undecidability (Slides 39-40).