function countVariables(expression) {
    const variablePattern = /x_\d+/g;
    const matches = expression.match(variablePattern);
    // Use a Set to store unique variables
    const uniqueVariables = new Set(matches);
    return uniqueVariables.size;
}

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
            const numberOfVariables = countVariables(data.expression_formatted.expression_problem);

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

            MathJax.typeset(); 

            if (numberOfVariables == 2) {

                document.getElementById('outputVal').innerText = 'Optimal value: ' + data['graph_method'].val;
                document.getElementById('outputVar').innerText = 'Coordinate: ('  + String(data['graph_method'].var[0]) +', ' + String(data['graph_method'].var[1]) + ')';
                MathJax.typeset(); // Typeset MathJax content after updating
            } else {
                document.getElementById('outputVar').textContent = '';
                document.getElementById('outputVal').textContent = '';
                document.getElementById('plotImage').remove();
                document.getElementsByClassName('result')[0].innerHTML = 'Cannot solve problem with many variables';
            }
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

            document.getElementById('outputVal2').innerText = 'Optimal value: ' + data['simplex_solver'].val;
            
            let variables = data['simplex_solver'].var;
            let output = 'Coordinate: (';
            for (let i = 0; i < variables.length; i++) {
                output += String(variables[i]);
                if (i < variables.length - 1) {
                    output += ', '; 
                }
            }

            output += ')';
            document.getElementById('outputVar2').innerText = output;

            
            let step_cnt = 0;
            let limited_length = jsonData.length;
            jsonData.forEach( (e) => {
                jsonData = JSON.parse(e);
                const jsonTable = document.createElement('table');
                if (jsonData.header.length !== 0 && jsonData.rows.length !== 0) {
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
                }
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