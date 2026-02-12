import time

class Tape:
    """
    Represents an infinite tape.
    """
    def __init__(self, contents=None):
        # Using a dictionary for infinite sparse storage. Key=index, Value=symbol
        self.tape = {} 
        self.head = 0
        if contents:
            for i, char in enumerate(contents):
                self.tape[i] = char

    def read(self):
        # Default to blank '_' if cell is empty
        return self.tape.get(self.head, "_")

    def write(self, symbol):
        self.tape[self.head] = symbol

    def move(self, direction):
        if direction == "R":
            self.head += 1
        elif direction == "L":
            self.head -= 1
    
    def get_content_string(self):
        # Helper to visualize the tape range
        if not self.tape:
            return "[Empty]"
        min_idx = min(self.tape.keys())
        max_idx = max(self.tape.keys())
        # Add buffer for visualization
        output = ""
        for i in range(min(0, min_idx), max(self.head, max_idx) + 2):
            val = self.tape.get(i, "_")
            if i == self.head:
                output += f"[{val}]"
            else:
                output += f" {val} "
        return output

class UniversalTuringMachine:
    """
    A 3-Tape Universal Turing Machine (UTM) [cite: 226-228].
    Tape 1: Description of M (encoded rules)
    Tape 2: Contents of M (input string)
    Tape 3: State of M (current state)
    """
    def __init__(self, machine_description, input_string, start_state="q1"):
        # Tape 1: Read-Only Description [cite: 239]
        self.tape1 = machine_description 
        
        # Tape 2: The Input/Work Tape 
        self.tape2 = Tape(list(input_string))
        
        # Tape 3: Internal State 
        # We store the *logical* state (e.g., 'q1') but can visualize it as binary '1'
        self.tape3 = Tape([start_state]) 
        
        # Hardcoded compiler maps for internal decoding
        self.state_to_bin = {"q1": "1", "q2": "11", "q3": "111"}
        self.sym_to_bin = {"_": "1", "1": "11", "0": "111"}
        
        # Reverse maps for decoding tape 1
        self.bin_to_dir = {"1": "R", "11": "L"}
        self.bin_to_state = {v: k for k, v in self.state_to_bin.items()}
        self.bin_to_sym = {v: k for k, v in self.sym_to_bin.items()}

    def step(self):
        """
        Executes one step of the simulation.
        1. Reads Tape 3 (State) and Tape 2 (Symbol).
        2. Encodes them to Binary (e.g., q1 -> 1, '1' -> 11).
        3. Scans Tape 1 for a matching pattern: state 0 symbol 0 ...
        4. Updates Tape 2 and Tape 3 based on the match.
        """
        current_state = self.tape3.tape.get(0) # State is at head of Tape 3
        current_symbol = self.tape2.read()
        
        # Convert to binary for matching on Tape 1
        # Example pattern to find: "10110" (State 1, Symbol 11)
        search_pattern_prefix = f"{self.state_to_bin[current_state]}0{self.sym_to_bin[current_symbol]}0"
        
        # Scan Tape 1 (The description)
        rules = self.tape1.split("00") # Split by rule separator
        
        found_rule = None
        for rule in rules:
            if rule.startswith(search_pattern_prefix):
                found_rule = rule
                break
        
        if not found_rule:
            return False # Halt (No transition defined)

        # Decode the Found Rule: state 0 read 0 next_state 0 write 0 move
        parts = found_rule.split("0")
        
        # Extract actions
        next_state_bin = parts[2]
        write_sym_bin = parts[3]
        move_dir_bin = parts[4]
        
        # Decode back to logical values
        next_state = self.bin_to_state[next_state_bin]
        write_sym = self.bin_to_sym[write_sym_bin]
        move_dir = self.bin_to_dir[move_dir_bin]
        
        # Apply updates [cite: 245]
        self.tape2.write(write_sym)        # Update Tape 2 (Content)
        self.tape2.move(move_dir)          # Move Head on Tape 2
        self.tape3.tape[0] = next_state    # Update Tape 3 (State)
        
        return True

    def run(self, max_steps=20, delay=0.5):
        print(f"\n{'='*20} INITIAL STATE {'='*20}")
        self.print_tapes()
        
        step_count = 0
        while step_count < max_steps:
            input("Press Enter to step...") # Interactive stepping
            running = self.step()
            step_count += 1
            
            print(f"\n{'='*20} STEP {step_count} {'='*20}")
            self.print_tapes()
            
            if not running:
                print("\n>>> Machine Halted (No Transition Found or Final State Reached) <<<")
                break
            
    def print_tapes(self):
        # Visualize the 3 tapes as per Slide 28
        print(f"Tape 1 (Desc): {self.tape1[:20]}... (Binary Encoded Rules)")
        print(f"Tape 2 (Work): {self.tape2.get_content_string()}")
        current_st = self.tape3.tape.get(0)
        st_bin = self.state_to_bin.get(current_st, "?")
        print(f"Tape 3 (Stat): [{current_st}] (Binary: {st_bin})")