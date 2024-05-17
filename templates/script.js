
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
    newInput.className = "calculator-input";
    newInput.placeholder = "Enter expression (e.g., x + 1 < 5)";
    newInput.required = true;
    newInput.id = "expression";
    newInput.setAttribute("onclick","handleClick(this)");
    newInput.autocomplete = "off";
    if (!document.getElementById('expression')) {
        container.insertBefore(newInput, document.getElementById('subject').nextSibling);
        return;
    }
    var currentInput = container.querySelector('#expression');
    container.insertBefore(newInput, currentInput.nextSibling);
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
    var expression = document.querySelectorAll("#expression");
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
        alert("Please enter an Problem Expression.");
        return false;
    }
    
    if (!areAllInputsEmpty(expression)) {
        alert("Please enter an Expression.");
        return false;
    }

    fetch('/validate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ expression: expression }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_valid) {
        ///

            var problem = document.getElementById("#problem-expression").value

        ///
        } else {
            alert("Invalid expression.");
        }
        console.log(data); // Log phản hồi từ server
    })
    .catch((error) => {
        console.error('Error:', error);
        alert("An error occurred.");
    });
}