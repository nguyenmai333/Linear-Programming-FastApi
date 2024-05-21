
var selectedElement = null;
function listen_user() {
    var number = prompt("Please enter a number:");
    if (number !== null) {
        var parsedNumber = parseFloat(number);
        if (!isNaN(parsedNumber)) {
            console.log("The user entered: " + parsedNumber);
        } else {
            console.log("Invalid input. Please enter a valid number.");
        }
    } else {
        console.log("User canceled the prompt.");
    }
    addCharacter('x_'+number)
}

function AddInputTag() {
    var container = document.querySelector('.expression-container');
    var newInput = document.createElement("input");
    newInput.type = "text";
    newInput.name = "expression";
    newInput.setAttribute("id", "expression")
    newInput.className = "calculator-input";
    newInput.placeholder = "Enter expression (e.g., x + 1 < 5)";
    newInput.setAttribute("onclick","handleClick(this)");
    newInput.required = true;
    newInput.autocomplete = "off";
    if (!document.getElementById('expression')) {
        container.insertBefore(newInput, document.getElementById('subject').nextSibling);
        return;
    }
    console.log(container)
    var currentInput = container.querySelectorAll('#expression');
    container.insertBefore(newInput, currentInput[currentInput.length - 1].nextSibling);
    return;
}
function DeleteInputTag() {
    if (!document.getElementById('expression')) {
        alert("There is no input field to delete.");
        return;
    }
    var container = document.querySelector('.expression-container');
    var currentInput = container.querySelector('#expression');
    container.removeChild(currentInput);
}

function handleClick(element) {
    var inputs = document.querySelectorAll('.calculator-input');
    inputs.forEach(function(input) {
        input.classList.remove('selected');
    });

    element.classList.add('selected');
    this.selectedElement = element
}

function addCharacter(character) {
    if (selectedElement) {
        var currentValue = selectedElement.value || "";
        selectedElement.value = currentValue + character;
    } else {
        alert("Please select an element first.");
    }
}

function confirmExpression() {
    var expressions = document.querySelectorAll("#expression");
    var problem_expression = document.getElementById("problem-expression");
    
    function areAllInputsEmpty(inputs) {
        for (var i = 0; i < inputs.length; i++) {
            if (inputs[i].value.trim() === "") {
                return false;
            }
        }
        return true;
    }

    if (problem_expression.value.trim() === "") {
        alert("Please enter a Problem Expression.");
        return false;
    }
    
    if (!areAllInputsEmpty(expressions)) {
        alert("Please enter all Expressions.");
        return false;
    }
    
    var expressionList = {};
    expressionList['problem'] = document.getElementById('problemSolver').value
    expressionList['expression_problem'] = problem_expression.value
    expressionList['constraints'] = []
    Array.from(expressions).forEach(function (expression) {
        expressionList['constraints'].push(expression.value);
    });
    fetch('/validate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ expression: JSON.stringify(expressionList)}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_valid) {
            console.log('Valid expression.');
            fetch('/calculate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {

            })
            .catch((e) => {
                console.error('error:', e);
                alert('Error');
            })
        } else {
            alert("Invalid expression.");
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert("An error occurred.");
    });
}
