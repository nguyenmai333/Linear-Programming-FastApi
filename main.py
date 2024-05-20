from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import uvicorn
from utils.formatter import jsonFormatter
from utils.validate_expression import isValidateExpression
import json

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Expression(BaseModel):
    expression: str

def preFormatConstraints(expr):
    print(expr)
    for id_, val in enumerate(expr):
      expr[id_] = isValidateExpression(val)
    return expr

# Endpoint
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/solve", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("solve.html", {"request": request})


@app.post("/calculate/")
async def calculate_expression(expression: Expression):
    try:
        expr = sympy.sympify(expression.expression)
        solution = sympy.solve_univariate_inequality(expr, "v")
        return {"solution": str(solution)}
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
        return {"is_valid": True, "expression_formatted": json_, "json_expression": json_formatted}
    except Exception as e:
        return {"is_valid": False, 'expression': []}
