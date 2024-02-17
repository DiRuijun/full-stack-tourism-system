const form = document.getElementById('searchForm');
const countryBar = document.getElementById('country-bar');
const placeBar = document.getElementById('place-bar');

form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const countryTerm = countryBar.value.trim();
    const placeTerm = placeBar.value.trim();
    if (placeTerm !== '' & countryTerm !== '') {
        try {
            const overviewInfoElement = document.getElementById('overviewInfo');
            overviewInfoElement.style.display = 'block'; 
            const overviewChartElement = document.getElementById('overviewChart');
            overviewChartElement.style.display = 'None';

            const response = await fetch(`/search?country=${countryTerm}&place=${placeTerm}`);
            
            if (response.ok) {
                const data = await response.json();
                document.getElementById('country').textContent = data.country;
                document.getElementById('placeTitle').textContent = data.place;
                document.getElementById('vote').textContent = data.vote;

                const commentBody = document.getElementById('commentBody');
                commentBody.innerHTML = ''; 
                data.comment.forEach((comment, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${comment['#']}</td><td>${comment.Content}</td>`;
                    commentBody.appendChild(row);
                }); 
            } else {
                const data = await response.json();
                alert('Error: '+ data.error);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
});
