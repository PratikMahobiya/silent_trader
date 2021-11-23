async function TransactionAPI() {
    let response = await fetch('http://139.59.54.145/crs30m/transactions_btst/')
    let data = await response.json();
    //returning the selected fields from the object getting from the response

    var userData = data.data.map(transaction => ({
        Time: convertFromStringToDate(transaction.date),
        Symbol: transaction.symbol,
        quantity: transaction.quantity,
        indicate: transaction.indicate,
        type: transaction.type,
        price: transaction.price,
        profit: transaction.profit,
        NiftyType: transaction.niftytype
    }));
    //console.log(userData);
    return userData;
}

async function ModelStatusAPI() {
    let response = await fetch('http://139.59.54.145/model_status/')
    let data = await response.json();
    //returning the selected fields from the object getting from the response

    var userData = data.data.map(status => ({
        model_name:         status.model_name,
        current_gain:       status.current_gain,
        date:               status.date,
        p_l:                status.p_l
    }));
    // console.log(userData);
    return userData;
}

async function PlaceOrderAPI(reference_id, symbol, price, quantity) {
    const data_place_order = { reference_id: reference_id ,symbol: symbol ,price: price ,quantity: quantity};
    // console.log(data_place_order);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // console.log('csrToken:- ', csrftoken);
    let response = await fetch('http://139.59.54.145/crs30m/place_order_btst/', {
    method: 'POST', // or 'PUT'
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(data_place_order),
    })
    let data = await response.json();
    // console.log(data);
    return data;
}


async function ExitOrderAPI(symbol) {
    const data_exit_order = {symbol: symbol};
    // console.log(data_exit_order);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // console.log('csrToken:- ', csrftoken);
    let response = await fetch('http://139.59.54.145/crs30m/exit_order_btst/', {
    method: 'POST', // or 'PUT'
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(data_exit_order),
    })
    let data = await response.json();
    // console.log(data);
    return data;
}

function ltp_color(Active){
    if (Active.price > Active.ltp){
        return "<b style='color:red;'>" + Active.ltp + '/' + (((Active.ltp - Active.price)/Active.price)*100).toFixed(2) + "</b>"
    }
    else if (Active.price < Active.ltp){
        return "<b style='color:green;'>" + Active.ltp + '/' + (((Active.ltp - Active.price)/Active.price)*100).toFixed(2) + "</b>"
    }
    if (Active.price == Active.ltp){
        return "<b style='color:black;'>" + Active.ltp + '/' + (((Active.ltp - Active.price)/Active.price)*100).toFixed(2) + "</b>"
    }
}

async function ActiveStocksAPI() {
    let response = await fetch('http://139.59.54.145/crs30m/active_stocks_btst/')
    let data = await response.json();
    //returning the selected fields from the object getting from the response
    var userData = data.data.map((Active, index) => ({
        Action: button_binding(index, Active),
        Time: convertFromStringToDate(Active.date),
        Symbol: Active.symbol,
        price: Active.price + '/' + ltp_color(Active),
        NiftyType: Active.niftytype,
        quantity: Active.quantity,
        sector: Active.sector.toUpperCase()
    }));
    //console.log(userData);
    return userData;
}


function button_binding(index, Active) {
    if (Active.placed == true) {
        return "<button type='submit' id='btn" + index + "' class='btn btn-sm' style='width:max-content; background-color:#FF0000;color:white' value='Submit' onclick=Exitmsg('" + Active.symbol + "')>EXIT_ Order</button>";
    } else {
        return "<button type='submit' id='btn" + index + "' class='btn btn-sm btn-primary' style='width:max-content' value='Submit' onclick=Successmsg(this,'" + Active.symbol + "','" + Active.ltp+ "','" + Active.quantity + "','" + Active.reference_id + "')>Place Order</button>";
    }
}


function getData() {
    // console.log("called");
    TransactionAPI().then(data =>
        CreateTableFromJSON(data) // this function will convert the json response to html table
    );
    ActiveStocksAPI().then(data =>
        CreateTableFromJSONActiveStocks(data) // this function will convert the json response to html table
    );
    ModelStatusAPI().then(data =>
        SetModelStatus(data) // this function will convert the json response to html table
    );
    setTimeout(function () { getData();}, 1000);
}

function SetModelStatus(data){
    for (var i = 0; i < data.length; i++) {
        var elem = document.getElementById(data[i].model_name);
        var elem_P_l = document.getElementById(data[i].model_name + '_%');
        var today_date = document.getElementById('TODAY_DATE');
        today_date.innerHTML = data[i].date;
        if (data[i].current_gain > 0){
            elem.setAttribute("style", "color:#2dc407;font-weight:500");
        }
        else if (data[i].current_gain < 0){
            elem.setAttribute("style", "color:Red;font-weight:500");
        }
        else if (data[i].current_gain == 0){
            elem.setAttribute("style", "font-weight:500");
        }
        
        if (data[i].p_l > 0){
            elem_P_l.setAttribute("style", "color:#2dc407;font-weight:500");
        }
        else if (data[i].p_l < 0){
            elem_P_l.setAttribute("style", "color:Red;font-weight:500");
        }
        else if (data[i].p_l == 0){
            elem_P_l.setAttribute("style", "font-weight:500");
        }
        elem.innerHTML = data[i].current_gain + ' ₹';
        elem_P_l.innerHTML = data[i].p_l + ' %';
    }
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
    table.setAttribute("style", "font-size:12px;width:48vw; margin-left:-9px");

    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.
    var tr = table.insertRow(-1);                   // TABLE ROW.
    for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th");      // TABLE HEADER.
        th.setAttribute("scope", "col");
        th.setAttribute("style", "background-color:#aea6a6;color:black;position: -webkit-sticky;position: sticky;top: 0;z-index: 1;");
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
            if (j === 0) {
                tabCell.innerHTML = data[i][col[j]];
                tabCell.setAttribute("style", "font-weight:900");
            }
            if (j === 1) {
                tabCell.innerHTML = data[i][col[j]];
                tabCell.setAttribute("style", "font-weight:700");
            }
            if (j === 3) {
                if (data[i][col[j]] === "Entry") {
                    tabCell.innerHTML = data[i][col[j]];
                    tabCell.setAttribute("style", "color:#2dc407;font-weight:900;text-transform: uppercase");
                }
                if (data[i][col[j]] === "Exit") {
                    tabCell.innerHTML = data[i][col[j]];
                    tabCell.setAttribute("style", "color:Red;font-weight:900;text-transform: uppercase");
                }
                
            }
            if (j === 5) {
                tabCell.innerHTML = data[i][col[j]];
                tabCell.setAttribute("style", "font-weight:bold");
            }
            if (j === 6) {
                var v = parseFloat(data[i][col[j]])

                if (v > 0) {
                    tabCell.innerHTML = data[i][col[j]];
                    tabCell.setAttribute("style", "color:#2dc407;font-weight:900");
                }
                else if (v < 0) {
                    tabCell.innerHTML = data[i][col[j]];
                    tabCell.setAttribute("style", "color:Red;font-weight:900");
                }
                else if (v == 0) {
                    tabCell.innerHTML = data[i][col[j]];
                    tabCell.setAttribute("style", "color:black;font-weight:900");
                }
            }
            else {
                tabCell.innerHTML = data[i][col[j]];
            }
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
    table.setAttribute("style", "font-size:14px;");

    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.
    var tr = table.insertRow(-1);                   // TABLE ROW.
    for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th");      // TABLE HEADER.
        th.setAttribute("scope", "col");
        th.setAttribute("style", "background-color:#aea6a6;color:black;position: -webkit-sticky;position: sticky;top: 0;z-index: 1;");
        if (i == 1) {
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
            if (j === 1) {
                tabCell.innerHTML = data[i][col[j]];
                tabCell.setAttribute("style", "font-weight:900");
            }
            if (j === 2) {
                tabCell.innerHTML = data[i][col[j]];
                tabCell.setAttribute("style", "font-weight:700");
            }
            if (j === 5) {
                tabCell.innerHTML = data[i][col[j]];
                tabCell.setAttribute("style", "font-weight:bold");
            }
            else {
                tabCell.innerHTML = data[i][col[j]];
            }
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

function Successmsg(button, symbol, price, quantity, reference_id) {
    Swal.fire({
        title: "Are you sure, you want to place an order for <b>" + symbol + "</b> ?",
        html:
            "<table style='text-align:left' cellpadding='6'>" +
            '<tr>' +
            '<td><b>Price</b></td>' + '<td><b>:</b></td>' + "<td><input type='text' class='form-control' id='price' value=" + price + "></tr>" +
            '<tr>' +
            '<td><b>Quantity</b></td>' + '<td><b>:</b></td>' + "<td><input type='text' class='form-control' id='quantity' value=" + quantity + ">" +
            '</tr>' +
            '</table>'
        ,

        showDenyButton: false,
        showCancelButton: true,
        confirmButtonText: 'Place Order',
        confirmButtonColor: '#0d6efd',
        denyButtonText: `Don't save`,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            var price = document.getElementById('price').value;
            var quantity = document.getElementById('quantity').value;
            PlaceOrderAPI(reference_id, symbol, price, quantity).then(data => {
                Swal.fire(
                    {
                        title: data.status,
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#0d6efd',
                    }
                )
                // document.getElementById(button.id).classList.remove("btn");
                // document.getElementById(button.id).classList.remove("btn-sm");
                // document.getElementById(button.id).classList.remove("btn-primary");

                // button.innerText = "Exit Order";
                // button.setAttribute("class", "btn btn-sm btn-danger");
            }
            );
        } else if (result.isDenied) {
            Swal.fire('Changes are not saved', '', 'info')
        }
    })
}
function Exitmsg(symbol) {
    Swal.fire({
        title: "Are you sure, you want to Exit an order for <b>" + symbol + "</b> ?",
        showDenyButton: false,
        showCancelButton: true,
        confirmButtonText: 'Exit Order',
        confirmButtonColor: '#FF0000',
        denyButtonText: `Don't save`,
    }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            ExitOrderAPI(symbol).then(data => {
                Swal.fire(
                    {
                        title: data.status,
                        confirmButtonText: 'OK',
                        confirmButtonColor: '#FF0000',
                    }
                )
            }
            );
        } else if (result.isDenied) {
            Swal.fire('Changes are not saved', '', 'info')
        }
    })
}
getData();