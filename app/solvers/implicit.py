# app/solvers/implicit.py
import re
import sympy as sp
from app.utils.latex_helpers import latex_to_sympy, sympy_to_latex

def differentiate_implicit(equation_latex: str, x_var: str = 'x', y_var: str = 'y') -> dict:
    """Solves for dy/dx using implicit differentiation."""
    try:
        # 1. Replace f(x) with y_var if present
        prep_latex = re.sub(r'f\([a-zA-Z]\)', y_var, equation_latex)

        # 2. Handle equations containing '=' by subtracting RHS from LHS (LHS - RHS = 0)
        if "=" in prep_latex:
            lhs_str, rhs_str = prep_latex.split("=", 1)
            lhs_expr = latex_to_sympy(lhs_str, strip_lhs=False)
            rhs_expr = latex_to_sympy(rhs_str, strip_lhs=False)
            expr = lhs_expr - rhs_expr
        else:
            expr = latex_to_sympy(prep_latex, strip_lhs=False)

        # 3. Define symbols
        x = sp.Symbol(x_var)
        y = sp.Symbol(y_var)

        # 4. Perform implicit differentiation using sp.idiff
        dydx = sp.idiff(expr, y, x)

        # 5. Convert result back to LaTeX
        output_latex = sympy_to_latex(dydx, simplify_first=True)

        return {
            "success": True,
            "input_latex": equation_latex,
            "result_latex": f"\\frac{{d{y_var}}}{{d{x_var}}} = " + output_latex
        }

    except Exception as e:
        return {
            "success": False,
            "input_latex": equation_latex,
            "error": f"Implicit differentiation failed: {str(e)}"
        }

# --- Terminal Test ---
if __name__ == "__main__":
    # Test: Circle equation x^2 + y^2 = 25
    test_eq = r"x^2 + y^2 = 25"
    result = differentiate_implicit(test_eq)
    
    print(f"Equation : {test_eq}")
    print(f"Result   : {result['result_latex']}")