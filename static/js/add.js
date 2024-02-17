document.getElementById("addPlaceForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    
    fetch('/add_place_of_interest', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                alert('Error:'+ data.error);
            });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return false;
});
