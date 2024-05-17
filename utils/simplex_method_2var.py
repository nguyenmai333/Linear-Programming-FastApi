from itertools import combinations
from read_json import from_json

class LinearProgrammingBasicSolver:
    def __init__(self, json_data):
        self.objective, self.constraints = from_json(json_data)
        self.points = []
        self.results = {}
    def intersection(self, m1, b1, m2, b2):
        if m1 == m2 and b1 == b2:
            return False
        elif m1 == m2:
            return False
        else:
            x = (b2 - b1) / (m1 - m2)
            y = m1 * x + b1
            if m1 != 0:
                return x, y
            elif b1 == 0:
                return x, 0
            else:
                return x, y

    def to_slope_intercept_form(self, constraint):
        lines = []
        coefficients = constraint['coefficients']
        a, b = coefficients[0], coefficients[1]
        if b != 0:
            m = -a / b
            b_value = constraint['rhs'] / b
            lines.append({'m': m, 'b': b_value})
        else:
            x_value = -constraint['rhs'] / a
            lines.append({'x': x_value})
        return lines

    def combinations_line(self):
        n = len(self.constraints)
        line_compare = list(combinations(range(0, n - 2), 2))
        self.points = []
        for li in line_compare:
            line1 = self.to_slope_intercept_form(self.constraints[li[0]])[0]
            line2 = self.to_slope_intercept_form(self.constraints[li[1]])[0]
            if self.intersection(line1['m'], line1['b'], line2['m'], line2['b']):
                self.points.append(self.intersection(line1['m'], line1['b'], line2['m'], line2['b']))
        for li in self.constraints[:n-2]:
            if li['coefficients'][1] != 0:
                self.points.append((0, li['rhs']/li['coefficients'][1]))
            if li['coefficients'][0] != 0:
                self.points.append((li['rhs']/li['coefficients'][0], 0))

    def isTruePoint(self, point):
        for constraint in self.constraints:
            val_ = constraint['coefficients'][0] * point[0] + constraint['coefficients'][1] * point[1]
            if constraint['relation'] == '<=':
                if val_ > constraint['rhs']:
                    return False
            if constraint['relation'] == '>=':
                if val_ < constraint['rhs']:
                    return False
        return True

    def findPoints(self):
        to_remove = [] 
        for id_, point in enumerate(self.points):
            if not self.isTruePoint(point):
                to_remove.append(id_)
        for id_ in reversed(to_remove):
            self.points.pop(id_)

        if points == []:
            print("bài toán vô nghiệm:")

    def find_optimal_value(self):
        max_val = self.objective['coefficients'][0] * self.points[0][0] + self.objective['coefficients'][1] * self.points[0][1]
        min_val = max_val
        recall_min = self.points[0]
        recall_max = recall_min

        for point in self.points:
            val = self.objective['coefficients'][0] * point[0] + self.objective['coefficients'][1] * point[1]
            if val < min_val:
                min_val = val
                recall_min = point
            if val > max_val:
                max_val = val
                recall_max = point

        if self.objective['type'] == 'max':
            print(f'Giá trị tối ưu: {max_val} | Nghiệm tối ưu: {recall_max}')
        else:
            print(f'Giá trị tối ưu: {min_val} | Nghiệm tối ưu: {recall_min}')

# Sử dụng class
json_data = {
    "objective": {
        "type": "max",
        "coefficients": [1, 1]
    },
    "constraints": [
        {
            "name": "constraint1",
            "coefficients": [1, 2],
            "relation": "<=",
            "rhs": 6
        },
        {
            "name": "constraint2",
            "coefficients": [2, 1],
            "relation": "<=",
            "rhs": 8
        },
        {
            "name": "constraint3",
            "coefficients": [0, 1],
            "relation": "<=",
            "rhs": 2
        },
        {
            "name": "constraint4",
            "coefficients": [1, 0],
            "relation": ">=",
            "rhs": 0
        }, 
        {
            "name": "constraint3",
            "coefficients": [0, 1],
            "relation": ">=",
            "rhs": 0
        }
    ]
}

lp_solver = LinearProgrammingSolver(json_data)
lp_solver.combinations_line()
lp_solver.findPoints()
lp_solver.find_optimal_value()
