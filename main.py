from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sympy

app = FastAPI(debug=True)
templates = Jinja2Templates(directory="templates")

class Expression(BaseModel):
    expression: str

# Endpoint
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/calculate/")
async def calculate_expression(expression: Expression):
    try:
        expr = sympy.sympify(expression.expression)
        solution = sympy.solve_univariate_inequality(expr, "v")
        return {"solution": str(solution)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/validate/")
async def validate_expression(expression: Expression):
    try:
        sympy.sympify(expression.expression)
        return {"is_valid": True}
    except Exception as e:
        return {"is_valid": False}
