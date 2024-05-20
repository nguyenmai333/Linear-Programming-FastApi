import sympy

def convert_to_subscript(expression):
    new_expression = ''
    i = 0
    while i < len(expression):
        new_expression += expression[i]
        if i < len(expression) - 1:
            if expression[i].isalpha() and expression[i+1].isdigit():
                new_expression += '_'
        i += 1
    return new_expression

def preprocess_expression(expr):
    new_expr = ''
    i = 0
    while i < len(expr):
        if expr[i].isdigit() and i < len(expr) - 1 and expr[i + 1].isalpha() and expr[i + 1].islower():
            new_expr += expr[i] + '*'
        elif expr[i].isalpha() and expr[i].islower() and i < len(expr) - 1 and expr[i + 1].isalpha() and expr[i + 1].islower():
            new_expr += expr[i] + '*'
        else:
            new_expr += expr[i]
        i += 1
    return convert_to_subscript(new_expr)

def isValidateExpression(expr):   
     try:
        corrected_preprocess_expression = preprocess_expression(expr)
        sympy.sympify(corrected_preprocess_expression)
        return corrected_preprocess_expression
     except Exception as e:
        return False
    