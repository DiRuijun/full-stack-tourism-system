document.getElementById('enterID').addEventListener('click', function() {
    var searchBarValue = document.getElementById('enterIDBar').value; 
    fetch(`/history?id=${searchBarValue}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('User not found');
        }
        return response.json();
    })
    .then(data => {
        var tbody = document.getElementById('historyBody'); 
        tbody.innerHTML = '';

        data.tableData.forEach(function(rowData) {
            var row = document.createElement('tr');
            Object.keys(rowData).forEach(function(key) {
                var cell = document.createElement('td'); 
                cell.textContent = rowData[key]; 
                row.appendChild(cell); 
            });    
            tbody.appendChild(row); 
        });
    })
    .catch(error => {
        alert('Error:'+ error);
    });
});
