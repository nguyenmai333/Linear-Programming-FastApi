function math_covert(val) {
    function formattedOperators(expression) {
        return expression.replace(/_/g, '')
                         .replace(/\*/g, '\\times ')
                         .replace(/<=/g, '\\le ');
    }
    val = formattedOperators(val);
    return val
}

function fetch_data() {
    const baseUrl = window.location.origin;
    const apiUrl = baseUrl + '/get_json/';
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const ExpressionList = data.expression_formatted.constraints;
            console.log(ExpressionList)
            const problemElement = document.getElementById('problem');
            const spanProblem = document.createElement('span');
            spanProblem.innerText = `\\(${'Problem: ' + data['expression_formatted'].problem + '(' + data['expression_formatted'].expression_problem + ')'}\\)`;
            problemElement.appendChild(spanProblem);
            
            for (const property in ExpressionList) {
                const formattedExpression = math_covert(ExpressionList[property]);
                const spanFormattedExpression = document.createElement('li');
                spanFormattedExpression.innerText = `\\(${formattedExpression}\\) `;
                problemElement.appendChild(spanFormattedExpression);
            }

            document.getElementById('outputVal').innerText = 'Optimal value: ' + data['graph_method'].val;
            document.getElementById('outputVar').innerText = 'Coordinate: ('  + String(data['graph_method'].var[0]) +', ' + String(data['graph_method'].var[1]) + ')';
            MathJax.typeset(); // Typeset MathJax content after updating
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            document.getElementById('output').innerText = 'Error: ' + error.message;
        });
}

function createSimplexSolverTable() {
    let jsonData = null
    const baseUrl = window.location.origin;
    const apiUrl = baseUrl + '/get_json/';
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            jsonData = data.simplex_solver.table[0];
            const tableHeaderRow = document.getElementById("tableHeader");
            jsonData = JSON.parse(jsonData)
            jsonData.header.forEach(header => {
                const th = document.createElement("th");
                th.textContent = header;
                tableHeaderRow.appendChild(th);
            });
            const tableBody = document.getElementById("tableBody");
            jsonData.rows.forEach(row => {
                const tr = document.createElement("tr");
                const tdName = document.createElement("td");
                tdName.textContent = row.name;
                tr.appendChild(tdName);
                row.values.forEach(value => {
                    const tdValue = document.createElement("td");
                    tdValue.textContent = value;
                    tr.appendChild(tdValue);
                });
                tableBody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}


fetch_data();
createSimplexSolverTable();