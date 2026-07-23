# app/solvers/taylor.py
import sympy as sp
from app.utils.latex_helpers import latex_to_sympy, sympy_to_latex

def calculate_taylor_series(
    latex_input: str, 
    var_str: str = 'x', 
    center: str = "0", 
    num_terms: int = 5
) -> dict:
    """
    Computes the Taylor series expansion of a LaTeX expression.
    
    Parameters:
        latex_input (str): The function to expand (e.g., r"\sin(x)")
        var_str (str): Variable of expansion (default 'x')
        center (str): The expansion point 'a' (default "0")
        num_terms (int): Number of order terms (n)
    """
    try:
        # 1. Parse input function and center point
        sympy_expr = latex_to_sympy(latex_input)
        center_expr = latex_to_sympy(str(center))
        var = sp.Symbol(var_str)

        # 2. Compute expansion and remove Big-O notation (+ O(x^n))
        taylor_series_expr = sympy_expr.series(
            var, 
            x0=center_expr, 
            n=num_terms
        ).removeO()

        # 3. Convert back to formatted LaTeX
        output_latex = sympy_to_latex(taylor_series_expr, simplify_first=True)

        return {
            "success": True,
            "input_latex": latex_input,
            "center": center,
            "num_terms": num_terms,
            "result_latex": output_latex
        }

    except Exception as e:
        return {
            "success": False,
            "input_latex": latex_input,
            "error": str(e)
        }


# --- Terminal Test ---
if __name__ == "__main__":
    print("=" * 50)
    print("  Taylor Series Solver Terminal Test")
    print("=" * 50)

    # Test 1: Maclaurin expansion of sin(x) around x=0 with 6 terms
    test_1 = r"\sin(x)"
    res1 = calculate_taylor_series(test_1, num_terms=6)
    print(f"\nFunction : {test_1} (around x=0)")
    print(f"Result   : {res1['result_latex']}")

    # Test 2: Taylor expansion of e^x around x=1 with 4 terms
    test_2 = r"e^x"
    res2 = calculate_taylor_series(test_2, center="1", num_terms=4)
    print(f"\nFunction : {test_2} (around x=1)")
    print(f"Result   : {res2['result_latex']}")