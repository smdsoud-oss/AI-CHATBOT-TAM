import sympy as sp
import re

def solve_math(problem):
    try:
        # Extract math expression from text
        # e.g. "solve x^2 + 5x + 6 = 0"
        problem = problem.lower()
        problem = re.sub(r'solve|calculate|find|what is', '', problem).strip()

        x = sp.Symbol('x')

        # Try to solve equation
        if '=' in problem:
            left, right = problem.split('=')
            expr = sp.sympify(left.strip()) - sp.sympify(right.strip())
            solution = sp.solve(expr, x)
            return f"x = {solution}"

        # Try to evaluate expression
        else:
            result = sp.sympify(problem)
            return f"= {sp.simplify(result)}"

    except Exception as e:
        return None  # Let the AI handle it instead