from io import BytesIO
import os
import json
import numpy as np
import matplotlib.pyplot as plt

def create_lambda_constraints(constraints):
    lambda_constraints = []
    for constraint in constraints:
        a, b = constraint['coefficients']
        relation = constraint['relation']
        c = constraint['rhs']
        
        if relation == '<=':
            lambda_constraints.append(lambda x, y, a=a, b=b, c=c: c - (a * x + b * y))
        elif relation == '>=':
            lambda_constraints.append(lambda x, y, a=a, b=b, c=c: (a * x + b * y) - c)
        else:
            raise ValueError(f"Unsupported relation: {relation}")
    
    return lambda_constraints

def graph_generator(lp_data):
    x = np.linspace(0, 8, 400)  
    y = np.linspace(0, 6, 400)  
    X, Y = np.meshgrid(x, y)
    lambda_constraints = create_lambda_constraints(lp_data['constraints'])     

    plt.contourf(X, Y, np.minimum.reduce([constraint(X, Y) for constraint in lambda_constraints]), cmap='Blues')

    for constraint in lambda_constraints[:-2]: 
        plt.contour(X, Y, constraint(X, Y), levels=[0], colors='red')
        

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Space satisfying constraints for quadratic polynomials')
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.xlim(0, 8)
    plt.ylim(0, 6)
    
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)
    
    return image_stream