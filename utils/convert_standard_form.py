import json

class StandardForm:
    def __init__(self, json_file: str) -> None:
        self._load_from_json(json_file)
        self.target = False
        self.smaller_constraint = False
        self.free = False
        self.original_target = []
    
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
        self.original_target = self.data["objective"]["coefficients"]
        # Xác định hàm mục tiêu
        if self.data["objective"]["type"] == "max":
            new_target = self.change_target(self.data["objective"]["coefficients"])
            P_2["objective"] = new_target
            self.target = True
        else:
            P_2["objective"] = self.data["objective"]
        
        num_of_consts = len(self.data["constraints"])
        num_of_variables = len(self.data["objective"]["coefficients"])
        
        # Danh sách để lưu các ràng buộc thỏa mãn điều kiện đặc biệt
        special_constraints = []

        for i in range(num_of_consts):
            relate = self.data["constraints"][i]["relation"]
            coefficients = self.data["constraints"][i]["coefficients"]
            rhs = self.data["constraints"][i]["rhs"]
            
            if coefficients.count(1) == 1 and coefficients.count(0) == (num_of_variables - 1) and rhs == 0:
                # Thêm ràng buộc vào danh sách đặc biệt
                special_constraints.append(self.data["constraints"][i])
                
            if relate == ">=":
                if not(coefficients.count(1) == 1 and coefficients.count(0) == (num_of_variables - 1) and rhs == 0):
                    new_dict = self.change_larger_equation(self.data["constraints"][i])
                    P_2["constraints"].append(new_dict)
    
            elif relate == "=":
                new_dict1, new_dict2 = self.change_equal_equation(self.data["constraints"][i], num_of_consts)
                P_2["constraints"].append(new_dict1)
                P_2["constraints"].append(new_dict2)
                num_of_consts += 1
            else:
                P_2["constraints"].append(self.data["constraints"][i])

        # Thêm các ràng buộc đặc biệt vào cuối danh sách
        pos_smaller_constraints = []
        if len(special_constraints) != 0:
            P_2["constraints"].extend(special_constraints)            
            # See if there is smaller contraint
            for i in range(num_of_variables):
                relate = P_2["constraints"][-(i+1)]["relation"]
                coefficients = P_2["constraints"][-(i+1)]["coefficients"]
                if relate == "<=":
                    self.smaller_constraint = True
                    pos = coefficients.index(1)
                    pos_smaller_constraints.append(pos)
                    P_2["constraints"][-(i+1)]["relation"] = ">="
                    
            for j in range(len(P_2["objective"]["coefficients"])):
                if j in pos_smaller_constraints:
                    P_2["objective"]["coefficients"][j] = -P_2["objective"]["coefficients"][j]
                    
            for i in range(num_of_consts):
                for j in pos_smaller_constraints:
                    P_2["constraints"][i]["coefficients"][j] = -P_2["constraints"][i]["coefficients"][j]
        else:
            self.free = True
            new_num_of_variables = 2*num_of_variables
            new_coefs = [0] * new_num_of_variables
            
            for i in range(num_of_variables):
                new_coefs[2*i] = P_2["objective"]["coefficients"][i]
                new_coefs[2*i + 1] = -P_2["objective"]["coefficients"][i] 
            P_2["objective"]["coefficients"] = new_coefs
            
            for i in range(num_of_consts):
                new_coefs = [0] * new_num_of_variables
                for j in range(num_of_variables):
                    new_coefs[2*j] = P_2["constraints"][i]["coefficients"][j]
                    new_coefs[2*j + 1] = -P_2["constraints"][i]["coefficients"][j]
                P_2["constraints"][i]["coefficients"] = new_coefs
                
            for i in range(new_num_of_variables):
                new_dict = {}
                new_dict["name"] = ""
                
                new_list = [1 if idx == i else 0 for idx in range(new_num_of_variables)]
                new_dict["coefficients"] = new_list
                
                new_dict["relation"] = ">="
                new_dict["rhs"] = 0
                P_2["constraints"].append(new_dict)
        return P_2, pos_smaller_constraints


    def to_standard_form(self):
        transformed_data, pos_smaller_constraints = self.transform()
        obj_func = transformed_data["objective"]["coefficients"] + [0] * (len(transformed_data["constraints"]) - len(transformed_data["objective"]["coefficients"]))
        coeffs = []
        constraints = []

        num_of_variables = len(transformed_data["objective"]["coefficients"])
        for i, constraint in enumerate(transformed_data["constraints"]):
            coefficients = constraint["coefficients"] + [0] * (len(obj_func) - len(constraint["coefficients"]))
            if i < (len(transformed_data["constraints"]) - len(transformed_data["objective"]["coefficients"])):
                coeffs.append(coefficients)
                coeffs[i][num_of_variables + i] = 1
                constraints.append(constraint["rhs"])

        return obj_func, coeffs, constraints, pos_smaller_constraints

