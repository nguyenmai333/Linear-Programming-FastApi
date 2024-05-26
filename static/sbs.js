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
    let jsonData = null;
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
            jsonData = data.simplex_solver.table;
            jsonStep = data.simplex_solver.step_info;
            let step_cnt = 0;
            let limited_length = jsonData.length;
            jsonData.forEach( (e) => {
                jsonData = JSON.parse(e);
                const jsonTable = document.createElement('table');
                jsonTable.id = 'jsonTable';
                
                const ele_thead = document.createElement('thead');
                ele_thead.setAttribute('id', 'tableHead');
                const ele_tbody = document.createElement('tbody');
                ele_tbody.setAttribute('id', 'tableBody');
                jsonTable.appendChild(ele_thead);
                jsonTable.appendChild(ele_tbody);
                
                // Creating the header row
                const tableHeaderRow = document.createElement("tr");
                tableHeaderRow.appendChild(document.createElement("th"));
                jsonData.header.forEach(header => {
                    const th = document.createElement("th");
                    th.textContent = header;
                    tableHeaderRow.appendChild(th);
                });
                
                ele_thead.appendChild(tableHeaderRow);
                // Creating the body rows
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
                    
                    ele_tbody.appendChild(tr);
                });
                document.getElementsByClassName('content')[1].appendChild(jsonTable);
                if (step_cnt < limited_length - 1) {
                    const step_info = document.createElement('div');
                    step_info.setAttribute('style','margin-left: 5%; margin-bottom: 1%;');
                    step_info.innerText = jsonStep[step_cnt];
                    document.getElementsByClassName('content')[1].appendChild(step_info);
                    step_cnt += 1;
                }
                
            })
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}



fetch_data();
createSimplexSolverTable();