"""Small HTTP calculator for the CI/CD exercise."""
import math
from flask import Flask, jsonify, request
app = Flask(__name__)

def calculate(operation, a, b):
    if isinstance(a, bool) or isinstance(b, bool) or not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("a and b must be numbers")
    if not math.isfinite(a) or not math.isfinite(b) or abs(a) > 1e12 or abs(b) > 1e12:
        raise ValueError("numbers must be finite and within +/- 1e12")
    if operation == "add": return a + b
    if operation == "subtract": return a - b
    if operation == "multiply": return a * b
    if operation == "divide":
        if b == 0: raise ValueError("division by zero")
        return a / b
    raise ValueError("unknown operation")

@app.get("/healthz")
def health():
    return jsonify(status="healthy")

@app.post("/calculate")
def endpoint():
    data = request.get_json(silent=True)
    if not isinstance(data, dict): return jsonify(error="JSON object required"), 400
    try: return jsonify(result=calculate(data.get("operation"), data.get("a"), data.get("b")))
    except (ValueError, OverflowError) as error: return jsonify(error=str(error)), 400
