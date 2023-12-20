
document.addEventListener('DOMContentLoaded', function (event) {
  console.log("function is workingg");
  var rows = document.querySelectorAll('.driver-row');

  rows.forEach(function (row) {
    row.addEventListener('click', function (event) {
      if (event.target.tagName.toLowerCase() === 'input') {
        // If it's an input, do nothing (or handle the input click as needed)
        return;
      }
      var driverId = row.getAttribute('data-driver-id');
      var url = driverDetailsUrl + driverId + '/details';
      window.location.href = url.replace('/details', '');
    });
  });
});

// Function to handle checkbox click
function handleCheckboxClick(checkbox) {
  // Stop the propagation of the click event to prevent navigation
  event.stopPropagation();
  // Get the row associated with the checkbox
  var row = checkbox.closest('.driver-row');

  // Toggle the 'selected' class on the row
  row.classList.toggle('selected');

  // Update the list of selected driver IDs
  updateSelectedDrivers();
}

function updateSelectedDrivers() {
  var selectedDrivers = document.querySelectorAll('.driver-row.selected');
  var driverIds = [];

  // Iterate over selected rows and extract driver IDs
  selectedDrivers.forEach(function (row) {
    var driverId = row.getAttribute('data-driver-id');
    driverIds.push(driverId);
  });

  // Update the hidden input with the selected driver IDs
  document.getElementById('driver_ids').value = JSON.stringify(driverIds);
}

function handleButtonClick(button) {
  event.stopPropagation();
  var row = button.closest('.driver-row');
  var editableCells = row.querySelectorAll('.editable');

  // Toggle visibility of text and input elements within the row
  editableCells.forEach(function (editableCell) {
    var spanElement = editableCell.querySelector('span');
    var inputElement = editableCell.querySelector('input');

    spanElement.style.display = spanElement.style.display === 'none' ? 'inline' : 'none';
    inputElement.style.display = inputElement.style.display === 'none' ? 'inline' : 'none';
  });
}

////

////second

function toggleAdvancedSearch() {
  var advancedSearchDiv = document.getElementById("advanced-search");
  advancedSearchDiv.style.display = (advancedSearchDiv.style.display === "none") ? "block" : "none";
  console.log("Advanced Search visibility:", advancedSearchDiv.style.display);
}

function saveAdvancedSearchState() {
  var advancedSearchDiv = document.getElementById("advanced-search");
  var isVisible = (advancedSearchDiv.style.display === "block");
  localStorage.setItem("advanced_search_visible", isVisible);

}

function saveAndSubmitForms() {
  saveAdvancedSearchState(); // Call your function to save advanced search state
  document.getElementById("paginationForm").submit(); // Submit the second form
}
// Function to save the selected value in local storage
function saveDriversPerPage() {
  var selectedValue = document.getElementById("drivers_per_page").value;
  localStorage.setItem("driversPerPage", selectedValue);
}

// Set the selected value when the page loads
// document.addEventListener("DOMContentLoaded", function () {
//   var savedValue = localStorage.getItem("driversPerPage");
//   if (savedValue !== null) {
//     document.getElementById("drivers_per_page").value = savedValue;
//   }
// });
// Restore advanced search state on page load
// Restore advanced search state on page load
window.onload = function () {
  var storedState = localStorage.getItem("advanced_search_visible");
  if (storedState === "true") {
    document.getElementById("advanced-search").style.display = "block";
  }
};

function toggleDetails(index) {
  var detailsRow = document.getElementById("details-" + index);
  detailsRow.style.display = (detailsRow.style.display === 'none') ? '' : 'none';
}

function deleteSelectedDrivers() {
  // Retrieve the list of selected driver IDs from the hidden input
  var driverIds = JSON.parse(document.getElementById('driver_ids').value);
  console.log("delete_function_isrunning")
  // Send the selected driver IDs to the server using AJAX
  fetch('/drivers/delete', {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json', // Add this line
    },
    body: JSON.stringify({ driver_ids: driverIds }),
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
  window.location.reload(true)
}
function updateBackend() {
  var rows = document.querySelectorAll('.driver-row');
  var updatedData = [];

  rows.forEach(function (row) {
    var driverId = row.getAttribute('data-driver-id');
    var forename = row.querySelector('.editable input[id="forename"]').value;
    var surname = row.querySelector('.editable input[id="surname"]').value;
    var driverRef = row.querySelector('.editable input[id="driverRef"]').value;
    var nationality = row.querySelector('.editable input[id="nationality"]').value;

    updatedData.push({
      driverId: driverId,
      forename: forename,
      surname: surname,
      driverRef: driverRef,
      nationality: nationality
      // Add more fields as needed
    });
  });

  // Make an AJAX request to update the backend
  fetch('drivers/update', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ data: updatedData }),
  })
    .then(response => response.json())
    .then(data => {
      // Handle the response from the server if needed
      console.log('Update successful', data);
    })
    .catch(error => {
      console.error('Error updating backend', error);
    });
    window.location.reload(true)
}
function onCreateDriver() {
  window.location.reload(true);
}