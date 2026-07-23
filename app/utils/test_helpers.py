# test_helpers.py
from latex_helpers import latex_to_sympy, sympy_to_latex

def run_interactive_tester():
    print("=" * 50)
    print("  LaTeX Converter Interactive Tester")
    print("  Type 'quit' or 'exit' to stop.")
    print("=" * 50)

    while True:
        try:
            # Get raw input from user
            user_input = input("\nEnter LaTeX expression: ").strip()
            
            # Check for exit command
            if user_input.lower() in ["quit", "exit"]:
                print("\nExiting tester. Bye!")
                break
            
            # Skip empty entries
            if not user_input:
                continue

            # Convert to SymPy
            parsed_expr = latex_to_sympy(user_input)
            print(f"  ├── SymPy Representation : {repr(parsed_expr)}")
            
            # Convert back to formatted LaTeX
            output_latex = sympy_to_latex(parsed_expr)
            print(f"  └── Converted Back LaTeX  : {output_latex}")

        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    run_interactive_tester()