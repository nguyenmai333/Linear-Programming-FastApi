# Author: Aru Bhoop
# Copyright: This module has been placed in the public domain.

import logging
import sys
from typing import List, Dict, Any

import numpy as np

from .exceptions import LinearlyDependentError
from .exceptions import SizeMismatchError
from .exceptions import UnsolvableError
from .tableau import Tableau


class SimplexSolver:
    """
    Solves a Linear Programming problem using Dantzig's Simplex Method
    by manipulating the `Tableau` class.

    Methods
    -------
    solve(max_iterations=100, use_blands_rule=False) : solves problem, yielding
    a`Solution` object

    """

    def __init__(self, obj_func: List[float], coeffs: List[List[float]], constraints: List[float]):
        """
        Assigns internal variables after performing basic checks.

        Parameters
        ----------
        obj_func: values af the objective function, in order. Must be of
           size *n* (n = number of variables).
        coeffs: values of technological coefficients (params), row-major.
          Must be size *m x n* (m = number of constraints)
        constraints: values of the constraint column-vector (right-hand
        side). Must be size *m*.
        """
        self.simplex_solver = {}
        self.simplex_solver["table"] = []
        self.simplex_solver["step_info"] = []
        self.step_by_step = {
            'table': [],
            'step_info': []
        }
        
        self.phase = False
        # validate dimensions
        m = len(constraints)  # rows
        n = len(obj_func)  # columns

        if len(coeffs) != m:
            raise SizeMismatchError
        for coeff in coeffs:
            if len(coeff) != n:
                raise SizeMismatchError

        # full rank assumption
        if m > n:
            raise LinearlyDependentError

        # create corresponding tableau
        self.tableau = Tableau(
            obj_func=obj_func,
            coeffs=coeffs,
            constraints=constraints
        )
        self.original_target = []
    
    def solve(self, max_iterations=10, use_blands_rule=False, print_tableau=True):
        """
        Solves Linear Programming Problem. Returns `Solution` instance`.

        Parameters
        ----------
        max_iterations : int
            Number of times to pivot before resorting to Bland's rule.
        use_blands_rule : bool
            Whether to use Bland's Rule for anti-cycling.
        print_tableau : bool
            Whether to print the tableau at every iteration.
        """

        # Configure logging
        logging.basicConfig(stream=sys.stdout,
                            format='%(message)s',
                            level=logging.DEBUG if print_tableau else logging.INFO)

        with self.tableau as t:
            
            if t.has_negative_rhs:
                logging.debug(f'{t}\n')
                self.step_by_step['table'].append(f'{t}')
                logging.info("Detect negative b. Use the 2-phase method")
                
                # Solve phase 1 problem
                t.add_artificial_variables()
                t.add_x0_to_tableau()
                logging.debug(f"\nAdd aritificial variable to first column of matrix")
                logging.debug(f'{t}\n')
                self.step_by_step['step_info'].append(f"Detect negative b. use the 2-phase method \n Add aritificial variable to first column of matrix")
                self.step_by_step['table'].append(f'{t}')
                self.phase = True
                logging.debug(f"\nPhase I Tableau:")
                r, c = t.pivot_around_2phase()
                logging.info(
                    f" Departing_Row: {r}, Entering_Col: {c}")
                logging.debug(f'{t}\n')
                self.step_by_step['step_info'].append(f" Departing_Row: {r}, Entering_Col: {c}")
                self.step_by_step['table'].append(f'{t}')
                self.solve(max_iterations=max_iterations)
                
            elif t.has_negative_coef and self.phase:
                t.pivot(use_blands_rule=use_blands_rule)
                logging.info(
                    f" Departing_Row: {t.pivot_idx[0]}, Entering_Col: {t.pivot_idx[1]}")  # Log pivots
                self.step_by_step['step_info'].append(f" Departing_Row: {t.pivot_idx[0]}, Entering_Col: {t.pivot_idx[1]}")
                self.step_by_step['table'].append(f'{t}')
                logging.debug(f'{t}\n')  # Log tableau
                self.solve(max_iterations=max_iterations)
    
            elif not(t.continue_phase_2) and self.phase:
                t.state = "Infeasible"
                
            elif not(t.has_negative_coef) and t.continue_phase_2 and self.phase:
                logging.debug(f'\nPhase II Tableau:')
                self.step_by_step['step_info'].append(f"\nPhase II Tableau \n New Target")
                t.change_target_2phase()   
                logging.debug(f'New target')      
                logging.debug(f'{t}\n')
                self.step_by_step['table'].append(f'{t}')
                iterations = 0
                # Keep pivoting until exception is raised or max iterations
                while iterations < max_iterations:
                    t.pivot(use_blands_rule=use_blands_rule)
                    logging.info(
                    f" Departing_Row: {t.pivot_idx[0]}, Entering_Col: {t.pivot_idx[1]}")  # Log pivots
                    self.step_by_step['step_info'].append(f" Departing_Row: {t.pivot_idx[0]}, Entering_Col: {t.pivot_idx[1]}")
                    logging.debug(f'{t}\n')  # Log tableau
                    self.step_by_step['table'].append(f'{t}')
                    iterations += 1

                # Resort to Bland's rule if necessary
                if not use_blands_rule:
                    logging.info("Possible Cycling detected. Resorting to Bland's Rule.")
                    self.step_by_step['step_info'].append(f"Possible Cycling detected. Resorting to Bland's Rule.")
                    return self.solve(use_blands_rule=True)

                # If no solution is found
                raise UnsolvableError(max_iterations)
                
                
            else:                
                logging.debug(f'{t}\n')
                self.step_by_step["table"].append(f'{t}')
                iterations = 0
                # Keep pivoting until exception is raised or max iterations
                while iterations < max_iterations:
                    t.pivot(use_blands_rule=use_blands_rule)
                    logging.info(
                    f" Departing_Row: {t.pivot_idx[0]}, Entering_Col: {t.pivot_idx[1]}")  # Log pivots
                    self.step_by_step['step_info'].append(f" Departing_Row: {t.pivot_idx[0]}, Entering_Col: {t.pivot_idx[1]}")
                    logging.debug(f'{t}\n')  # Log tableau
                    self.step_by_step['table'].append(f'{t}')
                    iterations += 1

                # Resort to Bland's rule if necessary
                if not use_blands_rule:
                    logging.info("Possible Cycling detected. Resorting to Bland's Rule.")
                    return self.solve(use_blands_rule=True)

                # If no solution is found
                raise UnsolvableError(max_iterations)

        return Solution(state=t.state, basis=t.basis,
                        solution=t.solution, obj_value=t.obj_value), self.step_by_step



class Solution:
    """
    Converts Tableau parameters into a human-readable solution.
    """

    def __init__(self, state: str, obj_value: float,
                 basis: List[int], solution: List[float]):
        """
        Calculates objective value and basic solution.

        Parameters
        ----------
        state : final state of the tableau
        obj_value : final objective value of tableau
        basis : indices of the basis variables
        solution : raw solution from tableau
        """
        self.state = state
        # objective value
        if obj_value != None:
            self.obj_value = {
                "Optimal": obj_value,
                "Unbounded": np.inf,
                "Infeasible": np.NaN
            }[self.state]

        # calculate solution if optimal
        if self.state == "Optimal":
            self.solution = [0.0] * (max(basis) + 1)  # start from zero vector
            for i, j in zip(basis, solution):
                self.solution[i] = j
        else:
            self.solution = None

    def __repr__(self):
        """
        Returns string representation of solution.
        """
        return 'Solution: ' + {
            "Optimal": f"z*={self.obj_value}, x*={self.solution}",
            "Unbounded": "The problem is unbounded.",
            "Infeasible": "The problem is infeasible."
        }[self.state]
