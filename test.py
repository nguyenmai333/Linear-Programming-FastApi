# File: run_simplex.py
import argparse
from utils.solver import SimplexSolver
from utils.convert_standard_form import StandardForm

def main(json_file):
    sf = StandardForm(json_file)
    obj_func, coeffs, constraints = sf.to_standard_form()
    solver = SimplexSolver(obj_func, coeffs, constraints)
    sol, step_by_step = solver.solve()

    if sf.target:
        sol.obj_value = -sol.obj_value
        print("Gia tri toi uu cua P:", sol.obj_value)
    else:
        print("Gia tri toi uu cua P:", sol.obj_value)
    print("Nghiem toi uu cua P:", sol.solution)

    print(step_by_step)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Simplex Solver on given JSON file.')
    parser.add_argument('json_file', type=str, help='Path to the JSON file containing the LPP data.')
    args = parser.parse_args()
    main(args.json_file)
