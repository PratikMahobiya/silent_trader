async function TransactionAPI() {
    //let response = await fetch('https://jsonplaceholder.typicode.com/users')
    // let response = await fetch('http://139.59.54.145/place_order/')
    // let response = await fetch('http://139.59.54.145/active_stocks/')
    let response = await fetch('http://139.59.54.145/transactions/')

    let data = await response.json();

    //returning the selected fields from the object getting from the response

    var userData = data.data.map(transaction => ({

        Time: convertFromStringToDate(transaction.date),
        Symbol: transaction.symbol,
        quantity: transaction.quantity,
        indicate:transaction.indicate,
        type:transaction.type,
        price: transaction.price,
        profit:transaction.profit,
        // pricedifference:transaction.difference,
        // sector: transaction.sector.toUpperCase(),
        NiftyType:"NA"

    }));
    //console.log(userData);
    return userData;
}

async function PlaceOrderAPI() {
    debugger;
    let response = await fetch('http://139.59.54.145/place_order/')
    let data = await response.json();
    //console.log(data);
    return data;
}



async function ActiveStocksAPI() {

    let response = await fetch('http://139.59.54.145/active_stocks/')

    let data = await response.json();

    //returning the selected fields from the object getting from the response

    var userData = data.data.map((Active,index) => ({
        Time: convertFromStringToDate(Active.date),
        Symbol: Active.symbol,
        sector: Active.sector.toUpperCase(),
        NiftyType: "NA",
        price: Active.price,
        quantity: Active.quantity,
        Action: "<button type='submit' id='btn" + index + "' class='btn btn-sm btn-primary' style='width:auto' value='Submit' onclick=Successmsg(this)>Place Order</button>",        
    }));
    //console.log(userData);
    return userData;
}

function getData() {
    console.log("called");
    TransactionAPI().then(data =>
        CreateTableFromJSON(data) // this function will convert the json response to html table
    );
    
       ActiveStocksAPI().then(data =>
        CreateTableFromJSONActiveStocks(data) // this function will convert the json response to html table
    );
    setTimeout(function () { getData();}, 1000);
}

function CreateTableFromJSON(data) {
    // EXTRACT VALUE FOR HTML HEADER. 
    // ('Book ID', 'Book Name', 'Category' and 'Price')
    var col = [];
    for (var i = 0; i < data.length; i++) {
        for (var key in data[i]) {
            if (col.indexOf(key) === -1) {
                col.push(key);
            }
        }
    }

    var table = document.createElement("table");

    table.setAttribute("class", "table table-striped table-hover");
    table.setAttribute("style", "font-size:12px;margin-left:-9px");

    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

    var tr = table.insertRow(-1);                   // TABLE ROW.

    for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th");      // TABLE HEADER.
        th.setAttribute("scope", "col");
        th.setAttribute("style", "background-color:#aea6a6;color:black");
        if (i == 0) {
            th.innerHTML = col[i] + "(24H)";
            tr.appendChild(th);
        }
        else {
            th.innerHTML = titleCase(col[i]);
            tr.appendChild(th);
        }
    }

    // ADD JSON DATA TO THE TABLE AS ROWS.
    for (var i = 0; i < data.length; i++) {

        tr = table.insertRow(-1);

        for (var j = 0; j < col.length; j++) {
            var tabCell = tr.insertCell(-1);
            tabCell.innerHTML = data[i][col[j]];
        }
    }
    // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
    var divContainer = document.getElementById("showDataActive");
    divContainer.innerHTML = "";
    divContainer.appendChild(table);
}

function CreateTableFromJSONActiveStocks(data) {
    var col = [];
    for (var i = 0; i < data.length; i++) {
        for (var key in data[i]) {
            if (col.indexOf(key) === -1) {
                col.push(key);
            }
        }
    }

    var table = document.createElement("table");

    table.setAttribute("class", "table table-striped table-hover");
    table.setAttribute("style", "font-size:12px;width: 40vw;margin-left:-9px");

    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

    var tr = table.insertRow(-1);                   // TABLE ROW.

    for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th");      // TABLE HEADER.
        th.setAttribute("scope", "col");
        th.setAttribute("style", "background-color:#aea6a6;color:black");
        if (i == 0) {
            th.innerHTML = col[i] + "(24H)";
            tr.appendChild(th);
        }
        else {
            th.innerHTML = titleCase(col[i]);
            tr.appendChild(th);
        }
    }

    // ADD JSON DATA TO THE TABLE AS ROWS.
    for (var i = 0; i < data.length; i++) {

        tr = table.insertRow(-1);

        for (var j = 0; j < col.length; j++) {
            var tabCell = tr.insertCell(-1);
            tabCell.innerHTML = data[i][col[j]];
        }
    }
    // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
    var divContainer = document.getElementById("showDataTransaction");
    divContainer.innerHTML = "";
    divContainer.appendChild(table);
}

function convertFromStringToDate(responseDate) {
    let dateComponents = responseDate.split('T');
    let datePieces = dateComponents[0].split("-");
    let timePieces = dateComponents[1].split(":");
    let SecondPieces = timePieces[2].split(".");

    var x = new Date(datePieces[2], (datePieces[1] - 1), datePieces[0],
        timePieces[0], timePieces[1], SecondPieces[0])
    var time = (x.getHours() < 10 ? '0' : '') + x.getHours() + ":" + (x.getMinutes() < 10 ? '0' : '') + x.getMinutes() + ":" + (x.getSeconds() < 10 ? '0' : '') + x.getSeconds()
    return (time)
}

function titleCase(str) {
    var splitStr = str.toLowerCase().split(' ');
    for (var i = 0; i < splitStr.length; i++) {
        // You do not need to check if i is larger than splitStr length, as your for does that for you
        // Assign it back to the array
        splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
    }
    // Directly return the joined string
    return splitStr.join(' ');
}

function Successmsg(button) {

    PlaceOrderAPI().then(data =>
        alert(data.status)
    );

    //Removing the previous style start

    document.getElementById(button.id).classList.remove("btn");
    document.getElementById(button.id).classList.remove("btn-sm");
    document.getElementById(button.id).classList.remove("btn-primary");

    //Removing the previous style end

    //Add the new style and change the text start
    button.innerText = "Exit";
    button.setAttribute("class", "btn btn-sm btn-danger");
    //Add the new style and change the text end 
}

getData();