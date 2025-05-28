export function Charge_results() {
    console.log("Search button clicked");
    const searchInput = document.getElementById('search-video').value;
    if (searchInput.trim() === '') {
        console.error('Search input is empty');
        return; // Exit if the search input is empty
    }
    console.log(`Searching for: ${searchInput}`);
    // Here you would typically make an API call to fetch search results
    // For example:
    // fetch(`/api/search?query=${searchInput}`)
    //   .then(response => response.json())
    //   .then(data => console.log(data))
    //   .catch(error => console.error('Error fetching search results:', error));
    const url = `http://localhost:5000/api/v1/search/?word=${searchInput}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Search results:', data);
            // Here you would update the state to display the results
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const downloadUrl = URL.createObjectURL(blob);
            const downloadLink = document.createElement('a');
            downloadLink.href = downloadUrl;
            downloadLink.download = 'search_results.json';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            URL.revokeObjectURL(downloadUrl);
        })
        .catch(error => console.error('Error fetching search results:', error));
}