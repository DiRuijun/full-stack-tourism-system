document.getElementById('get-id-btn').addEventListener('click', function() {
    fetch('/get_id')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById('id-display').innerText = data.id;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});