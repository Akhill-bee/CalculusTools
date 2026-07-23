# app/solvers/derivatives.py
import sympy as sp
from app.utils.latex_helpers import latex_to_sympy, sympy_to_latex

def differentiate_expression(latex_input: str, var_str: str = 'x', order: int = 1) -> dict:
    """
    Takes a raw LaTeX expression, differentiates it, and returns the result as LaTeX.
    
    Parameters:
        latex_input (str): The function to differentiate (e.g., r"\sin(x) + x^2")
        var_str (str): The variable to differentiate with respect to (default 'x')
        order (int): The order of the derivative (1 for 1st derivative, 2 for 2nd, etc.)
        
    Returns:
        dict: A dictionary containing success status, raw input, derivative LaTeX, and error messages.
    """
    try:
        # 1. Convert incoming LaTeX string to a SymPy expression
        sympy_expr = latex_to_sympy(latex_input)
        
        # 2. Define the differentiation variable
        var = sp.Symbol(var_str)
        
        # 3. Calculate the derivative (handles Chain, Product, Quotient, and Trig rules automatically!)
        derivative_expr = sp.diff(sympy_expr, var, order)
        
        # 4. Convert the result back to formatted LaTeX
        output_latex = sympy_to_latex(derivative_expr, simplify_first=True)
        
        return {
            "success": True,
            "input_latex": latex_input,
            "variable": var_str,
            "order": order,
            "result_latex": output_latex
        }

    except Exception as e:
        return {
            "success": False,
            "input_latex": latex_input,
            "error": str(e)
        }


# --- Interactive Terminal Test ---
if __name__ == "__main__":
    print("=" * 50)
    print("  Derivative Solver Terminal Test")
    print("=" * 50)

    # Test Case 1: Product / Chain Rule (x^2 * sin(x))
    test_1 = r"x^2 \sin(x)"
    res1 = differentiate_expression(test_1)
    print(f"\nFunction: {test_1}")
    print(f"1st Derivative: {res1['result_latex']}")

    # Test Case 2: Quotient Rule (\frac{x+1}{x-1})
    test_2 = r"\frac{x + 1}{x - 1}"
    res2 = differentiate_expression(test_2)
    print(f"\nFunction: {test_2}")
    print(f"1st Derivative: {res2['result_latex']}")

    # Test Case 3: 2nd Derivative of cos(x)
    test_3 = r"\cos(x)"
    res3 = differentiate_expression(test_3, order=2)
    print(f"\nFunction: {test_3} (2nd Derivative)")
    print(f"Result: {res3['result_latex']}")