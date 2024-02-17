document.getElementById("voteForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    
    fetch('/vote_for_place', {
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
        console.log(data)
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return false;
});