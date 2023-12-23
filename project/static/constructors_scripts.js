function handleCheckboxClick(checkbox) {
    // Stop the propagation of the click event to prevent navigation
    event.stopPropagation();
    // Get the row associated with the checkbox
    var row = checkbox.closest('.constructor-row');
    // Toggle the 'selected' class on the row
    row.classList.toggle('selected');
  
    // Update the list of selected constructor IDs
    updateSelectedConstructors();
  }

  function updateSelectedConstructors() {
  var selectedConstructors = document.querySelectorAll('.constructor-row.selected');
  var constructorIds = [];

  // Iterate over selected rows and extract constructors IDs
  selectedConstructors.forEach(function (row) {
    var constructorId = row.getAttribute('data-constructorId');
    constructorIds.push(constructorId);
  });

  // Update the hidden input with the selected driver IDs
  document.getElementById('constructorIds').value = JSON.stringify(constructorIds);
  console.log(constructorIds)
}

  function updateBackend() {
    var rows = document.querySelectorAll('.constructor-row');
    var updatedData = [];

    rows.forEach(function (row) {
        var constructorId = row.getAttribute('data-constructorId');
        var constructorRef = row.querySelector('.editable input[id="constructorRef"]').value;
        var name = row.querySelector('.editable input[id="name"]').value;
        var nationality = row.querySelector('.editable input[id="nationality"]').value;
        var url = row.querySelector('.editable input[id="url"]').value;

        updatedData.push({
        constructorId: constructorId,
        constructorRef: constructorRef,
        name: name,
        nationality: nationality,
        url: url
        // Add more fields as needed
        });
    });

    // Make an AJAX request to update the backend
    fetch('http://127.0.0.1:5000/constructors/update', {
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



function handleButtonClick(button) {
    event.stopPropagation();
    var row = button.closest('.constructor-row');
    var editableCells = row.querySelectorAll('.editable');

    // Toggle visibility of text and input elements within the row
    editableCells.forEach(function (editableCell) {
        var spanElement = editableCell.querySelector('span');
        var inputElement = editableCell.querySelector('input');

        //spanElement.style.display = spanElement.style.display === 'none' ? 'inline' : 'none';
        inputElement.style.display = inputElement.style.display === 'none' ? 'inline' : 'none';
    });
}

function deleteSelected() {
  // Retrieve the list of selected driver IDs from the hidden input
  var constructorIds = JSON.parse(document.getElementById('constructorIds').value);
  // Send the selected driver IDs to the server using AJAX
  fetch('/constructors/delete', {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json', // Add this line
    },
    body: JSON.stringify({ constructorIds: constructorIds }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Success: ', data);
      // Optionally, update the UI or perform other actions based on the server response
    })
    .catch((error) => {
      console.error('Error:', error);
      // Handle errors as needed
    });
  window.location.reload(true)
}

document.addEventListener('DOMContentLoaded', function () {
    var rows = document.querySelectorAll('.toggle-row');
    rows.forEach(function (row) {
        row.addEventListener('click', function () {
            // Toggle visibility of the next row with class 'more-details'
            var detailsRow = row.nextElementSibling;
            detailsRow.style.display = (detailsRow.style.display === 'none') ? 'table-row' : 'none';
        });
    });
});
