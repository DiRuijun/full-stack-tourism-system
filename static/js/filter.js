document.getElementById('filter').addEventListener('click', function() {
    var searchBarValue = document.getElementById('searchBar').value; 

    fetch(`/filter_by_country?country=${searchBarValue}`)
    .then(async response => {
        if (!response.ok) {
            const data = await response.json();
            alert('Error: ' + data.error);
            throw new Error('Place not found');
        } else {
            const data_1 = await response.json();
            var tbody = document.getElementById('filterBody');
            tbody.innerHTML = '';
            data_1.tableData.forEach(function (rowData) {
                var row = document.createElement('tr');
                Object.keys(rowData).forEach(function (key) {
                    var cell = document.createElement('td');
                    cell.textContent = rowData[key];
                    row.appendChild(cell);
                });
                tbody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});



