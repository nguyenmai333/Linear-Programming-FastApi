import json

class StandardForm:
    def __init__(self, json_file: str) -> None:
        self._load_from_json(json_file)
        self.target = False
    
    def _load_from_json(self, json_file: str) -> None:
        with open(json_file, 'r') as file:
            self.data = json.load(file)

    def change_target(self, coefs):
        new_target = "min"
        new_coef = [-x for x in coefs]
        return {"type": new_target, "coefficients": new_coef}

    def change_larger_equation(self, old_constraint):
        new_coef = [-x for x in old_constraint["coefficients"]]
        new_rhs = -old_constraint["rhs"]
        return {"name": old_constraint["name"], "coefficients": new_coef, "relation": "<=", "rhs": new_rhs}

    def change_equal_equation(self, old_constraint, index):
        new_coef = [-x for x in old_constraint["coefficients"]]
        new_rhs = -old_constraint["rhs"]
        dict_1 = {"name": old_constraint["name"], "coefficients": old_constraint["coefficients"], "relation": "<=", "rhs": old_constraint["rhs"]}
        dict_2 = {"name": f"constraint{index+1}", "coefficients": new_coef, "relation": "<=", "rhs": new_rhs}
        return dict_1, dict_2

    def transform(self):
        P_2 = {"objective": {}, "constraints": []}
        
        # Xác định hàm mục tiêu
        if self.data["objective"]["type"] == "max":
            new_target = self.change_target(self.data["objective"]["coefficients"])
            P_2["objective"] = new_target
            self.target = True
        else:
            P_2["objective"] = self.data["objective"]
        
        num_of_consts = len(self.data["constraints"])
        num_of_variables = len(self.data["objective"]["coefficients"])
        
        for i in range(num_of_consts):
            relate = self.data["constraints"][i]["relation"]
            coefficients = self.data["constraints"][i]["coefficients"]
            rhs = self.data["constraints"][i]["rhs"]

            # Điều kiện loại bỏ trường hợp có hệ số [0, 1] hoặc [1, 0] và rhs = 0
            if relate == ">=" and not (coefficients.count(1) == 1 and coefficients.count(0) == (num_of_variables - 1) and rhs == 0):
                new_dict = self.change_larger_equation(self.data["constraints"][i])
                P_2["constraints"].append(new_dict)
            elif relate == "=":
                new_dict1, new_dict2 = self.change_equal_equation(self.data["constraints"][i], num_of_consts)
                P_2["constraints"].append(new_dict1)
                P_2["constraints"].append(new_dict2)
                num_of_consts += 1
            else:
                P_2["constraints"].append(self.data["constraints"][i])

        return P_2

    def to_standard_form(self):
        transformed_data = self.transform()
        obj_func = transformed_data["objective"]["coefficients"] + [0] * (len(transformed_data["constraints"]) - len(transformed_data["objective"]["coefficients"]))
        coeffs = []
        constraints = []

        j = 0
        num_of_variables = len(transformed_data["objective"]["coefficients"])
        for i, constraint in enumerate(transformed_data["constraints"]):
            coefficients = constraint["coefficients"] + [0] * (len(obj_func) - len(constraint["coefficients"]))
            if not (coefficients.count(1) == 1 and coefficients.count(0) == (len(obj_func) - 1) and constraint["rhs"] == 0):
                coeffs.append(coefficients)
                coeffs[j][num_of_variables + j] = 1
                constraints.append(constraint["rhs"])
                j += 1

        return obj_func, coeffs, constraints


