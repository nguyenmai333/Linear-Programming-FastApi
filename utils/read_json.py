
def from_json(json_data):
    objective = json_data["objective"]
    constraints = json_data["constraints"]
    return objective, constraints
