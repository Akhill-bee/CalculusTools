# app/solvers/integrals.py
import sympy as sp
from app.utils.latex_helpers import latex_to_sympy, sympy_to_latex

def integrate_expression(
    latex_input: str, 
    var_str: str = 'x', 
    lower_bound: str = None, 
    upper_bound: str = None
) -> dict:
    """
    Computes indefinite or definite integrals using SymPy.
    
    Parameters:
        latex_input (str): Function to integrate (e.g., r"\sin(x)")
        var_str (str): Integration variable (default 'x')
        lower_bound (str, optional): Lower limit of integration for definite integrals
        upper_bound (str, optional): Upper limit of integration for definite integrals
    """
    try:
        # 1. Convert LaTeX input to SymPy
        sympy_expr = latex_to_sympy(latex_input)
        var = sp.Symbol(var_str)

        # 2. Definite Integral (Bound values provided)
        if lower_bound is not None and upper_bound is not None:
            a = latex_to_sympy(str(lower_bound))
            b = latex_to_sympy(str(upper_bound))
            
            # SymPy syntax: sp.integrate(expr, (variable, lower, upper))
            integral_expr = sp.integrate(sympy_expr, (var, a, b))
            output_latex = sympy_to_latex(integral_expr, simplify_first=True)
            
            return {
                "success": True,
                "type": "definite",
                "input_latex": latex_input,
                "bounds": [lower_bound, upper_bound],
                "result_latex": output_latex
            }

        # 3. Indefinite Integral
        else:
            integral_expr = sp.integrate(sympy_expr, var)
            output_latex = sympy_to_latex(integral_expr, simplify_first=True)
            
            # Append constant of integration (+ C) for indefinite integrals
            final_latex = output_latex + " + C"

            return {
                "success": True,
                "type": "indefinite",
                "input_latex": latex_input,
                "result_latex": final_latex
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
    print("  Integral Solver Terminal Test")
    print("=" * 50)

    # Test 1: Indefinite Integral (\int x^2 \cdot \cos(x) dx)
    test_1 = r"x^2 \cos(x)"
    res1 = integrate_expression(test_1)
    print(f"\nIndefinite Integral of: {test_1}")
    print(f"Result: {res1['result_latex']}")

    # Test 2: Definite Integral (\int_0^{\pi} \sin(x) dx)
    test_2 = r"\sin(x)"
    res2 = integrate_expression(test_2, lower_bound="0", upper_bound=r"\pi")
    print(f"\nDefinite Integral of: {test_2} from 0 to \\pi")
    print(f"Result: {res2['result_latex']}")