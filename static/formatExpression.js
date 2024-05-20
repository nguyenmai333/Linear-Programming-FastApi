document.addEventListener('DOMContentLoaded', () => {
    const operators = ['2*x_1 + 2*x_2 <= 5', '3*x_1 <= 6'];
    const operatorsDiv = document.getElementById('operators');

    // Chuyển đổi các toán tử thành định dạng LaTeX
    const formattedOperators = operators.map(operator => {
        return operator.replace(/_/g, '')
                       .replace(/\*/g, '\\times ')
                       .replace(/<=/g, '\\le ');
    });

    // Tạo các phần tử span chứa các biểu thức toán học và thêm vào thẻ div
    formattedOperators.forEach(operator => {
        const operatorSpan = document.createElement('span');
        operatorSpan.textContent = `\\(${operator}\\)`;
        operatorsDiv.appendChild(operatorSpan);
        operatorsDiv.appendChild(document.createElement('br')); // Thêm xuống dòng
    });

    // Yêu cầu MathJax xử lý lại các biểu thức toán học
    MathJax.typeset();
});
