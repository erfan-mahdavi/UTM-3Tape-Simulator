import sys
import argparse
from src.compiler import TMCompiler
from src.utm import UniversalTuringMachine

def main():
    print(">>> 3-Tape Universal Turing Machine Simulator <<<")
    print("Based on Dept. of Computer Science, Theory of Computation Course\n")

    # 1. Setup Argument Parser
    parser = argparse.ArgumentParser(description="Run a UTM simulation.")
    parser.add_argument('file', help="Path to the JSON machine file (e.g., examples/increment.json)")
    parser.add_argument('input', help="Input string for the machine (e.g., '111')")
    args = parser.parse_args()

    # 2. Compile the Machine
    print(f"[Compiler] Reading machine definition from {args.file}...")
    compiler = TMCompiler()
    try:
        machine_code, start_state = compiler.compile(args.file)
        print(f"[Compiler] Success! Machine Encoded to Binary.")
        print(f"[Debug] Tape 1 Content: {machine_code}\n")
    except Exception as e:
        print(f"[Error] Compilation failed: {e}")
        return

    # 3. Initialize the UTM
    utm = UniversalTuringMachine(
        machine_description=machine_code, 
        input_string=args.input, 
        start_state=start_state
    )

    # 4. Run Simulation
    print(f"[UTM] Loading Tapes...")
    print(f"[UTM] Input String on Tape 2: '{args.input}'")
    utm.run()

if __name__ == "__main__":
    main()