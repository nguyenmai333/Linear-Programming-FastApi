import json
import re

class jsonFormatter:
    def __init__(self, problem):
        self.problem = problem

    def count_variables(self):
        variables = re.findall(r'x\d+', self.problem['expression_problem'])
        return len(set(variables))
    
    def find_signs_positions(self, expression):  # Added self here
        signs_positions = {}
        matches = re.finditer(r'([+-]?)\s*(\d*\.?\d*\s*)?(x\d+)', expression)
        indices = []
        for match in matches:
            sign = match.group(1)
            coefficient = match.group(2)
            if sign == '':
                sign = '+'
            if coefficient == '':
                coefficient = '1'
            indices.append(int(match.group(3)[1:]))
            signs_positions[int(match.group(3)[1:])] = (sign, float(coefficient))
        return signs_positions, indices
    
    def extract_coefficients(self, expression, num_var):
        coefficients_list = [0] * num_var
        signs, _ = self.find_signs_positions(expression)
        for key, val in signs.items():
            coefficients_list[key - 1] = val[1]
            if val[0] == '-':
                coefficients_list[key - 1] *= -1
        return coefficients_list

    def transform_to_json(self):
        num_var = self.count_variables()
        input_json = {
            "objective": {
                "type": self.problem["problem"],
                "coefficients": self.extract_coefficients(self.problem["expression_problem"], num_var)
            },
            "constraints": [
                {
                    "name": "constraint{}".format(i + 1),
                    "coefficients": self.extract_coefficients(constraint, num_var),
                    "relation": "<=" if "<=" in constraint else ">=",
                    "rhs": int(constraint.split()[-1])
                }
                for i, constraint in enumerate(self.problem["constraints"])
            ]
        }
        return input_json

# problem = {'problem': 'max', 'expression_problem': 'x1 + x2', 'constraints': ['x1 >= 0', 'x2 >= 0', 'x1 + x2 <= 5']}

# transformer = jsonFormatter(problem)
# input_json = transformer.transform_to_json()
# print(json.dumps(input_json, indent=4))
