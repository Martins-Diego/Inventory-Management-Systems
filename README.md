# Inventory Management Systems

## Business Problem

Effective inventory management is a critical issue for many businesses in today's fast-paced market. Companies face the challenge of handling growing volumes of data and meeting increasing market demands, making the task of finding the right software or solution for efficient inventory management essential. According to a study by the Wasp Barcode Technologies, around 43% of small businesses either do not track inventory or use manual methods, which can lead to inefficiencies and stock discrepancies. Furthermore, businesses often struggle to identify the best solution tailored to their specific needs, particularly in terms of company size. This report will present two inventory management solutions: a VBA-based system targeting smaller businesses and a web-based platform designed for larger enterprises handling greater data volumes, providing a comprehensive analysis of their respective benefits and applications.

## Solution 1 - VBA with User Form

![vba_inventory_panel.png](https://raw.githubusercontent.com/Martins-Diego/Inventory-Management-Systems/main/vba_inventory_panel.png)

**Sub1 definition of variables** 

```vbnet
  Dim lastRow As Long
  Dim i As Long
  Dim product_code As String
  Dim description As String
  Dim price_per_unit As Integer
  Dim quantity As Integer
```

**Store TextBox values within variables** 

```vbnet
product_code = UserForm2.Controls("TextBox1").Value
description = UserForm2.Controls("TextBox2").Value
price_per_unit = UserForm2.Controls("TextBox3").Value
quantity = UserForm2.Controls("TextBox4").Value
```

**Add and Edit products** 

```vbnet
lastRow = Hoja1.Cells(Rows.Count, 2).End(xlUp).Row + 1
For i = 3 To lastRow
'if code already exists
     If Hoja1.Cells(i, 2).Value = product_code Then
       Hoja1.Cells(i, 2).Value = product_code
       Hoja1.Cells(i, 3).Value = description
       Hoja1.Cells(i, 4).Value = Hoja1.Cells(i, 4).Value + quantity
       Hoja1.Cells(i, 6).Value = Hoja1.Cells(i, 4).Value - Hoja1.Cells(i, 5).Value
       Hoja1.Cells(i, 7).Value = "$" & Format(price_per_unit, "#,##0.00")
       Hoja1.Cells(i, 8).Value = "$" & Format((Hoja1.Cells(i, 6).Value * Hoja1.Cells(i, 7).Value), "#,##0.00")
       Exit For
'if code doesnt exist
     ElseIf Hoja1.Cells(i, 2).Value = "" Then
       Hoja1.Cells(i, 2).Value = product_code
       Hoja1.Cells(i, 3).Value = description
       Hoja1.Cells(i, 4).Value = quantity
       Hoja1.Cells(i, 5).Value = 0
       Hoja1.Cells(i, 6).Value = Hoja1.Cells(i, 4).Value - Hoja1.Cells(i, 5).Value
       Hoja1.Cells(i, 7).Value = "$" & Format(price_per_unit, "#,##0.00")
       Hoja1.Cells(i, 8).Value = "$" & Format((Hoja1.Cells(i, 6).Value * Hoja1.Cells(i, 7).Value), "#,##0.00")
       Exit For
    End If
Next
```

**Sub2 definition of variables**

```vbnet
Dim lastRow As Long
Dim i As Long
Dim product_code As String
Dim quantity As Integer
Dim foundProduct As Boolean
```

**Outgoing products logic**

```vbnet
For i = 3 To lastRow
	If Hoja1.Cells(i, 2).Value = product_code Then
	  If quantity > Hoja1.Cells(i, 4).Value - Hoja1.Cells(i, 5).Value Then
	    MsgBox "The quantity of outgoing products must be equal or less than the stock available (" & (Hoja1.Cells(i, 4).Value - Hoja1.Cells(i, 5).Value) & ")."
      Exit Sub
      End If
      Hoja1.Cells(i, 5).Value = Hoja1.Cells(i, 5).Value + quantity
      Hoja1.Cells(i, 5).HorizontalAlignment = xlCenter
      foundProduct = True
      Exit For
   End If
Next i

If foundProduct Then
	For i = 3 To lastRow
	  If Hoja1.Cells(i, 2).Value = product_code Then
		   Hoja1.Cells(i, 6).Value = Hoja1.Cells(i, 4).Value - Hoja1.Cells(i, 5).Value
       Hoja1.Cells(i, 8).Value = "$" & Format((Hoja1.Cells(i, 6).Value * Hoja1.Cells(i, 7).Value), "#,##0.00")
		End If
  Next i
Else
  MsgBox "Product not found in inventory."
End If
```

**Command buttons verifications** 

```vbnet
If Trim(TextBox1.Value) = "" Or Trim(TextBox2.Value) = "" Or Trim(TextBox3.Value) = "" Or Trim(TextBox4.Value) = "" Then
	MsgBox "Complete all the fields to add or edit a product"
	Exit Sub
End If
Call add_product
End Sub
```

**Logic behind delete button** 

```vbnet
For i = 3 To lastRow
	If Hoja1.Cells(i, 2).Value = product_code Then
	  Hoja1.Rows(i).Delete
    MsgBox "Product deleted successfully."
    Exit Sub
  End If
Next i
MsgBox "Product not found in inventory."
```

**Criterium to clear form fields**

```vbnet
UserForm2.Controls("TextBox1").Value = ""
UserForm2.Controls("TextBox2").Value = ""
UserForm2.Controls("TextBox3").Value = ""
UserForm2.Controls("TextBox4").Value = ""
```

**Onchange method for user experience**

```vbnet
' Search the product code on the inventory
    For i = 3 To Hoja1.Cells(Rows.Count, 2).End(xlUp).Row
        If Hoja1.Cells(i, 2).Value = product_code Then
            description = Hoja1.Cells(i, 3).Value
            price_per_unit = Hoja1.Cells(i, 7).Value
            Exit For
        End If
    Next i
    
    ' Update the textbox values
    TextBox2.Value = description
    If price_per_unit = 0 And description = "" Then
        TextBox3.Value = ""
    Else
        TextBox3.Value = price_per_unit
    End If
```

### System Testing

## Solution 2 - Web Based Solution

![web_solution_ss](https://raw.githubusercontent.com/Martins-Diego/Inventory-Management-Systems/main/web_solution_ss)

### State Transfer Diagram

![state_transfer_diagram.png](https://raw.githubusercontent.com/Martins-Diego/Inventory-Management-Systems/main/state_transfer_diagram.png)

1. Imagine that a user fills in the form fields on the web page, including the Product Code, Description, Unit Price, and Quantity.
2. When this user clicks on the "Add Product" button, a JavaScript function is triggered. The function sends an HTTP request to the web server ([app.py](http://app.py/)) using the fetch() method. In this case, the values of the form fields are submitted in a FormData object.
3. The web server ([app.py](http://app.py/)) receives the HTTP request and processes it. In this case, the request goes to the route defined in the decorator @app.route('/add', methods=['POST']).
4. The function that handles this route in ([app.py](http://app.py/)) extracts the values from the FormData object and uses them to insert a new row into the "inventory" table of the MySQL database.
5. The function in (app.py) returns an HTTP response with a JSON object that indicates whether the operation was successful or not.
6. The JavaScript file processes the HTTP response. If the operation was successful, it adds a new row to the webpage table with the entered product values. Otherwise, it displays an alert with the corresponding error message.
7. Similar logic was applied to develop the other functionalities of the system.

### MySQL Inventory Database

![mysql_inventory_db.png](https://raw.githubusercontent.com/Martins-Diego/Inventory-Management-Systems/main/mysql_inventory_db.png)

```python
# Establish connection with the MySQL database
def db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="admin",
        database="inventory_db",
        cursorclass=pymysql.cursors.DictCursor)
```

### Local Web Server Deployment

![local_web_server_deployment.png](https://raw.githubusercontent.com/Martins-Diego/Inventory-Management-Systems/main/local_web_server_deployment.png)

### AJAX Request Example

```jsx
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
```

### Database Values Insertion

```python
@app.route('/add', methods=['POST'])
def add_product():
    conn = db_connection()
    cursor = conn.cursor()

    #Get the data from the submitted form
    product_code = request.form['product_code']
    description = request.form['description']
    price_per_unit = request.form['price_per_unit']
    quantity = request.form['quantity']

    # Calculate stock values and inventory amount
    stock = int(quantity) 
    inventory_amount = float(price_per_unit) * stock

    # Verify if the product already exists in the db
    cursor.execute("SELECT * FROM inventory WHERE product_code = %s", (product_code,))
    product_exists = cursor.fetchone()

    if not product_exists:
        # If the product does not exist, insert the data into the database table
        cursor.execute("INSERT INTO inventory (product_code, descrip, price_per_unit, entries, issues, stock, inventory_amount) VALUES (%s, %s, %s, %s, 0, %s, %s)", (product_code, description, price_per_unit, quantity, stock, inventory_amount))
        conn.commit()
        status = "success"
    else:
        status = "error"

    # Close the conecction
    cursor.close()
    conn.close()
    # Returns a success or error response depending on the case
    return jsonify({"status": status})
```

### System Testing

## Benefits

### Solution 1 - VBA with User Form

1. **Cost-effectiveness:** As VBA is part of Microsoft Office, many small businesses already have access to it, eliminating the need for additional software investments.
2. **User-friendliness:** The user interface is simple and intuitive, minimizing the need for extensive employee training.
3. ****Customization:**** The system can be easily tailored to the unique needs of individual businesses, offering a flexible and adaptable solution

### Solution 2 - JS/Python/MySQL

1. **Scalability**: The web-based system is designed to accommodate larger data volumes and scale effortlessly with business growth.
2. **Accessibility:** The system can be accessed from any device with an internet connection, enabling remote access and real-time updates.
3. **Integration**: This solution can be readily integrated with other systems, such as accounting or ERP software, for a more streamlined and efficient business process.
