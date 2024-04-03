const perspective = require("@finos/perspective");
const WebSocket = require("ws");

// Replace with the appropriate WebSocket server URL
const server_url = "ws://localhost:8080/websocket";

// Create a new WebSocket
const ws = new WebSocket(server_url);

ws.on("open", function open() {
    console.log("Connected to Perspective server.");
    
    // Create a new perspective client over the WebSocket
    const client = new perspective.client(ws);

    // Load or create a table
    // Note: Adjust "table_name" to match the actual table you're interested in
    client.open_table("data_source_one").then(async table => {
        console.log("Table opened.");
        
        // Example: Creating a view to listen for updates
        const view = await table.view({
            // Configure your view here
            // Example configuration: columns, aggregates, filters, sorts, etc.
        });
        
        // Fetching initial data
        const initialData = await view.to_json();
        console.log("Initial data:", initialData);
        
        // Listening for updates (this example does not handle updates explicitly)
        // You can listen to 'perspective-update' events on the view if needed
        view.on_update(() => {
            console.log("Table updated.");
            // Optionally, fetch new data on update
            // view.to_json().then(data => console.log("Updated data:", data));
        }, {mode: "row"}); // Adjust the update mode as needed

    }).catch(err => {
        console.error("Error opening table:", err);
    });
});

ws.on("error", function error(err) {
    console.error("WebSocket error:", err);
});
