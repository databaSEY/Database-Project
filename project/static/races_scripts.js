function toggleAdvancedSearch() {
    var advancedSearchDiv = document.getElementById("advanced-search");
    advancedSearchDiv.style.display = (advancedSearchDiv.style.display === "none") ? "block" : "none";
    saveAdvancedSearchState();
}

function saveAdvancedSearchState() {
    var advancedSearchDiv = document.getElementById("advanced-search");
    var isVisible = (advancedSearchDiv.style.display === "block");
    localStorage.setItem("advanced_search_visible", isVisible);
}

// Restore advanced search state on page load
window.onload = function() {
    var storedState = localStorage.getItem("advanced_search_visible");
    console.log("Stored State:", storedState);

    if (storedState === "true") {
        console.log("Setting advanced-search to block");
        document.getElementById("advanced-search").style.display = "block";
    }
};

function toggleDetails(index) {
    var detailsRow = document.getElementsByClassName("details-" + index);
    for (var i = 0; i < detailsRow.length; i++) {
        detailsRow[i].style.display = (detailsRow[i].style.display === 'none') ? '' : 'none';
    }
}

function map_ltln(lat, lon, mapId) {
    // Initialize the map with a unique ID5
    var map = L.map(mapId).setView([lat, lon], 10)
    // Add a tile layer (you can choose different providers)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Add a marker at the specified coordinates
    L.marker([lat, lon]).addTo(map);
}

function deleteSelectedRaces() {
    // Retrieve the list of selected driver IDs from the hidden input
    var race_ids = JSON.parse(document.getElementById('race_ids').value);
    console.log("delete_function_isrunning")
    // Send the selected driver IDs to the server using AJAX
    fetch('/races/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json', // Add this line
            },
            body: JSON.stringify({
                race_ids: race_ids
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            // Optionally, update the UI or perform other actions based on the server response
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle errors as needed
        });
    window.location.reload()
}
// Function to handle checkbox click
function handleCheckboxClick(checkbox) {
    // Stop the propagation of the click event to prevent navigation
    event.stopPropagation();
    // Get the row associated with the checkbox
    var row = checkbox.closest('.race-row');

    // Toggle the 'selected' class on the row
    row.classList.toggle('selected');

    // Update the list of selected driver IDs
    updateSelectedRaces();
}

function updateSelectedRaces() {
    var selectedRaces = document.querySelectorAll('.race-row.selected');
    var raceIds = [];

    // Iterate over selected rows and extract driver IDs
    selectedRaces.forEach(function(row) {
        var raceId = row.getAttribute('data-race-id');
        raceIds.push(raceId);
    });

    // Update the hidden input with the selected driver IDs
    document.getElementById('race_ids').value = JSON.stringify(raceIds);
}

function handleButtonClick(button, index) {
    event.stopPropagation();

    // Get all rows with the class '.race-row'
    var rows = document.querySelectorAll('.edit-' + index);

    // Loop through each row
    rows.forEach(function(row) {
        var editableCells = row.querySelectorAll('.editable');

        // Toggle visibility of text and input elements within the row
        editableCells.forEach(function(editableCell) {
            var spanElement = editableCell.querySelector('span');
            var inputElement = editableCell.querySelector('input');

            spanElement.style.display = spanElement.style.display === 'none' ? 'inline' : 'none';
            inputElement.style.display = inputElement.style.display === 'none' ? 'inline' : 'none';
        });
    });
}


function updateBackend() {
    var rows = document.querySelectorAll('.update-row');
    var updatedData = [];
    console.log(rows);
    var sw = 0;
    rows.forEach(function(row) {
            // Switch statement
            switch (sw) {
                case 0:
                    var raceId = row.getAttribute('data-race-id');
                    var circuitId = row.getAttribute('data-circuit-id');
                    var r_name = row.querySelector('.editable [id="r_name"]').value;
                    var r_year = row.querySelector('.editable [id="r_year"]').value;
                    var c_country = row.querySelector('.editable [id="c_country"]').value;
                    sw = 1;
                    break;
                case 1:
                    var r_date = row.querySelector('.editable [id="r_date"]').value;
                    var r_round = row.querySelector('.editable [id="r_round"]').value;
                    var c_location = row.querySelector('.editable [id="c_location"]').value;
                    sw = 2;
                    break;

                case 2:
                    var c_name = row.querySelector('.editable [id="c_name"]').value;
                    sw = 0;
                    break;
            }
            updatedData.push({
                raceId: raceId,
                r_name: r_name,
                r_year: r_year,
                r_date: r_date,
                r_round: r_round,
                circuitId: circuitId,
                c_name: c_name,
                c_location: c_location,
                c_country: c_country
                // Add more fields as needed
            });

        }

    );

    // Make an AJAX request to update the backend
    fetch('/races/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                data: updatedData
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server if needed
            console.log('Update successful', data);
        })
        .catch(error => {
            console.error('Error updating backend', error);
        });
}
