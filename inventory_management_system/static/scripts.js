function AddData() {
    // Get the values of the form fields
    const productCode = document.getElementById("product-code").value;
    const description = document.getElementById("description").value;
    const pricePerUnit = document.getElementById("price-per-unit").value;
    const quantity = document.getElementById("quantity").value;

    // Create a FormData object to send the data
    const formData = new FormData();
    formData.append("product_code", productCode);
    formData.append("description", description);
    formData.append("price_per_unit", pricePerUnit);
    formData.append("quantity", quantity);

    // Make an AJAX request to add the data
    fetch("/add", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Updates the view (for example, adds a row to the table)
            const table = document.getElementById("crudTable");
            const newRow = table.insertRow(-1);

            newRow.insertCell(0).innerHTML = productCode;
            newRow.insertCell(1).innerHTML = description;
            newRow.insertCell(2).innerHTML = quantity; // Entries
            const issues = 0; // Issues
            newRow.insertCell(3).innerHTML = issues;
            newRow.insertCell(4).innerHTML = quantity - issues; // Stock (Entries - Issues)
            newRow.insertCell(5).innerHTML = pricePerUnit;
            newRow.insertCell(6).innerHTML = (quantity - issues) * pricePerUnit; // Inventory Amount

            // Clear form fields
            ClearFields();
        } else {
            alert("The product is already on the inventory");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function ClearFields() {
    document.getElementById("product-code").value = "";
    document.getElementById("description").value = "";
    document.getElementById("price-per-unit").value = "";
    document.getElementById("quantity").value = "";
}

function IssueData() {
    // Get the values of the form fields
    const productCode = document.getElementById("product-code").value;
    const description = document.getElementById("description").value;
    const pricePerUnit = document.getElementById("price-per-unit").value;
    const quantity = document.getElementById("quantity").value;

    // Create a FormData object to send the data
    const formData = new FormData();
    formData.append("product_code", productCode);
    formData.append("description", description);
    formData.append("price_per_unit", pricePerUnit);
    formData.append("quantity", quantity);

    // Make an AJAX request to update the data
    fetch("/issue", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            const table = document.getElementById("crudTable");
            for (let i = 1; i < table.rows.length; i++) {
                if (table.rows[i].cells[0].innerHTML === productCode) {
                    // Updates the values of the corresponding row
                    const entries = parseInt(table.rows[i].cells[2].innerHTML);
                    const issues = parseInt(table.rows[i].cells[3].innerHTML) + parseInt(quantity);
                    const stock = entries - issues;
                    const inventoryAmount = stock * parseFloat(pricePerUnit);
                    table.rows[i].cells[3].innerHTML = issues;
                    table.rows[i].cells[4].innerHTML = stock;
                    table.rows[i].cells[6].innerHTML = inventoryAmount;
                    break;
                }
            }
            
            // Clear form fields
            ClearFields();
        } else {
            alert("Error al actualizar el producto");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}