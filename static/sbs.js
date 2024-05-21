function get_data() {
    const baseUrl = window.location.origin;
    console.log('Base URL:', baseUrl);
    const apiUrl = baseUrl + '/get_json/';
    console.log('API URL:', apiUrl);
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data:', data);

            // Display the data on the webpage
            document.getElementById('outputVar').innerText = 'Var: ' + data.var;
            document.getElementById('outputVal').innerText = 'Val: ' + JSON.stringify(data.val, null, 2);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            // Display an error message on the webpage
            document.getElementById('output').innerText = 'Error: ' + error.message;
        });
}

get_data();
