// script.js
// This file contains the JavaScript code for the IP Watcher frontend.

$(document).ready(function() {
    // Initialize the DataTable.
    $('#devices').DataTable({
        // Load data from the API.
        "ajax": "/api/devices",
        // Define the columns to display.
        "columns": [
            { "data": "id" },
            { "data": "ip_address" },
            { "data": "mac_address" },
            { "data": "vendor" },
            { "data": "os" },
            { "data": "open_ports" },
            { "data": "first_seen" },
            { "data": "last_seen" }
        ]
    });
});
