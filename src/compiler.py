import json

class TMCompiler:
    """
    Converts a human-readable Turing Machine definition into the 
    binary encoding specified in the Theory of Computation slides.
    
    Encoding Standard [Slide 38]:
    - States: q1 -> 1, q2 -> 11, etc.
    - Symbols: a1 (blank) -> 1, a2 (1) -> 11, etc.
    - Directions: R -> 1, L -> 11
    - Separator: 0
    - Rule Separator: 00
    """

    def __init__(self):
        # Mappings based on Slide 38 [cite: 284, 288]
        self.direction_map = {"R": "1", "L": "11"}
        # a1 is blank, a2 is '1'
        self.symbol_map = {"_": "1", "1": "11", "0": "111"} 
        # q1 is start, q2 is halt usually
        self.state_map = {"q1": "1", "q2": "11", "q3": "111"}

    def encode_rule(self, rule):
        """
        Encodes a single transition rule: T(curr_q, read) -> (next_q, write, move)
        Format: curr_q 0 read 0 next_q 0 write 0 move
        """
        try:
            curr_q_bin = self.state_map[rule['q']]
            read_bin = self.symbol_map[rule['read']]
            next_q_bin = self.state_map[rule['next_q']]
            write_bin = self.symbol_map[rule['write']]
            move_bin = self.direction_map[rule['move']]
            
            # Combine with '0' separators [cite: 220]
            encoded = f"{curr_q_bin}0{read_bin}0{next_q_bin}0{write_bin}0{move_bin}"
            return encoded
        except KeyError as e:
            raise ValueError(f"Unknown symbol or state in rule: {e}. Check your JSON maps.")

    def compile(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        encoded_rules = []
        for rule in data['transitions']:
            encoded_rules.append(self.encode_rule(rule))
        
        # Rules are separated by '00' 
        # Example output for Rule A + Rule B: 1011010110100101011011011
        full_machine_code = "00".join(encoded_rules)
        return full_machine_code, data['initial_state']