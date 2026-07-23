# app/utils/latex_helpers.py
import re
import sympy as sp
from sympy.parsing.latex import parse_latex

def clean_latex_string(latex_str: str, strip_lhs: bool = True) -> str:
    """Strips whitespace, function notations (f(x)=, y=), and cleans input."""
    if not latex_str:
        raise ValueError("Empty input string")
    
    cleaned = latex_str.strip()

    # If input is in explicit form like "f(x) = x^2" or "y = x^2", extract the right-hand side
    if strip_lhs and "=" in cleaned:
        lhs, rhs = cleaned.split("=", 1)
        # Check if LHS is just a variable or function like y, f(x), g(t)
        if re.match(r"^\s*([a-zA-Z](\([a-zA-Z]\))?)\s*$", lhs):
            cleaned = rhs.strip()

    return cleaned


def latex_to_sympy(latex_str: str, strip_lhs: bool = True) -> sp.Expr:
    """Parses a raw LaTeX string into a SymPy expression object."""
    try:
        cleaned_str = clean_latex_string(latex_str, strip_lhs=strip_lhs)
        expr = parse_latex(cleaned_str)
        return expr
    except Exception as e:
        raise ValueError(f"Invalid LaTeX syntax: {str(e)}")


def sympy_to_latex(expr: sp.Expr, simplify_first: bool = True) -> str:
    """Converts a SymPy expression back into a formatted LaTeX string."""
    if simplify_first:
        expr = sp.simplify(expr)
    return sp.latex(expr)

if __name__ == "__main__":
    # Test execution
    test_input = r"\sin(x) + \frac{x^2}{2}"
    print("Testing input:", test_input)
    
    parsed = latex_to_sympy(test_input)
    print("SymPy Object:", repr(parsed))
    
    output_latex = sympy_to_latex(parsed)
    print("Output LaTeX:", output_latex)