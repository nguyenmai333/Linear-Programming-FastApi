import json
import re

class jsonFormatter:
    def __init__(self, problem):
        self.problem = problem

    def count_variables(self):
        variables = re.findall(r'x\d+', self.problem['expression_problem'])
        return len(set(variables))

    def extract_coefficients(self, expression, num_var):
        coefficients_list = [0] * num_var
        coefficients = re.findall(r'([-+]?\d*\.*\d*)\*?x(\d+)', expression)
        for val, id_ in coefficients:
            id_ = int(id_)
            if val == '':
                coefficients_list[id_ - 1] = float(1)
            else:
                coefficients_list[id_ - 1] = float(val)
        return coefficients_list

    def transform_to_json(self):
        num_var = self.count_variables()
        input_json = {
            "objective": {
                "type": self.problem["problem"],
                "coefficients": [1] * num_var
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

# problem = {
#     "problem": "max",
#     "expression_problem": "x1 + x2",
#     "constraints": [
#         "x1 + 2*x2 <= 6",
#         "x2 >= 0",
#         "x2 <= 2",
#         "2*x1 + x2 <= 8",
#         "x1 >= 0"
#     ]
# }

# transformer = jsonFormatter(problem)
# input_json = transformer.transform_to_json()

# print(json.dumps(input_json, indent=4))
