from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import requests
from io import BytesIO
from utils.formatter import jsonFormatter
from utils.validate_expression import isValidateExpression
from utils.simplex_method_2var import LinearProgrammingBasicSolver
from utils.graph_plot import graph_generator
from utils.solver import SimplexSolver
from utils.convert_standard_form import StandardForm
import re

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

###global result
stored_result = {}
image_stream = None

class Expression(BaseModel):
    expression: str


def splitTable(table):
    pos_ = table.find('RHS') + len('RHS')
    left, right = table[:pos_], table[pos_:]
    header = left.split(' ')
    header.pop(0)
    pattern = re.compile(r'(\w+)\s+\[([-\d.\s]+)\]')
    matches = pattern.findall(right)
    rows = []
    for name, values in matches:
        values_list = values.split()
        row = {
            "name": name,
            "values": values_list
        }
        rows.append(row)
    structured_data = {
        "header": header,
        "rows": rows
    }
    structured_data["header"] = [item for item in structured_data["header"] if item]
    return json.dumps(structured_data, indent=4)

def simplexSolver(data):
    sf = StandardForm(data)
    obj_func, coeffs, constraints = sf.to_standard_form()
    solver = SimplexSolver(obj_func, coeffs, constraints)
    sol, step_by_step = solver.solve()
    formatted_table = []
    for i in step_by_step['table']:
        formatted_table.append(splitTable(i))
    step_by_step['table'] = formatted_table
    if sf.target:
        sol.obj_value = -sol.obj_value
        print("Gia tri toi uu cua P:", sol.obj_value)
    else:
        print("Gia tri toi uu cua P:", sol.obj_value)
    print("Nghiem toi uu cua P:", sol.solution)


    return step_by_step, sol.obj_value, sol.solution
    
def preFormatConstraints(expr):
    for id_, val in enumerate(expr):
      expr[id_] = isValidateExpression(val)
    return expr

def graph_method(data):
    lp_solver = LinearProgrammingBasicSolver(data)
    lp_solver.combinations_line()
    lp_solver.findPoints()
    lp_solver.find_optimal_value()
    return lp_solver.results
# Endpoint
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/solve", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("solve.html", {"request": request})

@app.post("/calculate/")
async def calculate_expression(data: dict):
    global stored_result
    global image_stream
    try:
        json_loader = json.loads(data['json_expression'])
        res = graph_method(json_loader)
        simplex_solver_res = simplexSolver(json_loader)
        image_stream = graph_generator(json_loader)
        stored_result['graph_method'] = res
        stored_result['simplex_solver'], stored_result['simplex_solver']['val'], stored_result['simplex_solver']['var'] = simplex_solver_res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/validate")
async def validate_expression(expression: Expression):
    try:
        json_ = json.loads(expression.expression)
        Formatter = jsonFormatter(json_)
        json_formatted = Formatter.transform_to_json()
        json_formatted = json.dumps(json_formatted, indent=4)
        json_['constraints'] = preFormatConstraints(json_['constraints'])
        json_['expression_problem'] = isValidateExpression(json_['expression_problem'])
        stored_result['expression_formatted'] = json_
        stored_result['json_expression'] = json_formatted
        return {"is_valid": True, "expression_formatted": json_, "json_expression": json_formatted}
        
    except Exception as e:
        return {"is_valid": False, 'expression': []}


@app.get("/get_json/")
async def get_json():
    global stored_result
    if stored_result:
        return stored_result
    else:
        raise HTTPException(status_code=404, detail="No result available")

@app.get("/graph/")
async def get_image():
    global image_stream
    if image_stream:
        return Response(content=image_stream.getvalue(), media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="No result available")
