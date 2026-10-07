import pytest
from app.calculator import app, calculate

@pytest.mark.parametrize("op,a,b,expected", [("add",2,3,5),("subtract",2,3,-1),("multiply",2,3,6),("divide",6,3,2)])
def test_operations(op,a,b,expected):
    assert calculate(op,a,b)==expected

@pytest.mark.parametrize("op,a,b", [("divide",1,0),("other",1,2),("add",True,1),("add","1",2),("add",float("inf"),2)])
def test_invalid(op,a,b):
    with pytest.raises(ValueError):calculate(op,a,b)

def test_http_contract():
    c=app.test_client()
    assert c.get('/healthz').status_code==200
    assert c.post('/calculate',json={'operation':'add','a':3,'b':4}).json=={'result':7}
    assert c.post('/calculate',json=[]).status_code==400
