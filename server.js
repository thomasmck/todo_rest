// Originally based on https://courses.ideate.cmu.edu/48-739/s2017/?page_id=177

// Include express and create app
var express = require('express');
var app = express();


// Include and initiate bodyParser for handling POST
var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));

// Include and initiate pug
app.set('view engine', 'pug');
const pug = require('pug');

// Include http
var http = require("http");

//Load html template
var fs = require("fs");

// options for REST API get
// Should look at packages that do this, i.e.
// https://www.npmjs.com/package/node-rest-client
var options = {
    host: "127.0.0.1",
    port: 5000,
    path: '/todo',
    method: 'GET'
};

// Get function
app.get('/', function(req, res) {
    // Request latest todo list from REST API
    // Update REST options for GET
    options['method'] = "GET";
    options['path'] = "/todo";
    http.request(options, function(res2) {
        res2.setEncoding('utf8');
        res2.on('data', function(chunk) {
            json_chunk = JSON.parse(chunk);
            json_chunk_array = json_chunk['task'];
            res.render('index', { title: 'Hey', message: json_chunk_array });
        });
    }).end();
});

// POST function
app.get('/CREATE', function(req, res) {
    // Request latest todo list from REST API
    // Update REST options for GET
    res.render('create');
});

app.post('/CREATE/new', function(req, res) {
    json = req.body;
    // Update REST options for POST
    options['method'] = "POST";
    options['path'] = "/todo";
    options['headers'] = { 'content-type': 'application/json' };
    var req2 = http.request(options, function(res) {
        console.log("STATUS: " + res.statusCode);
        console.log("HEADERS: " + JSON.stringify(res.headers));
        res.setEncoding("utf8");
        res.on("data", function(chunk) {
            console.log("BODY: " + chunk);
        });
    });
    req2.on("error", function(e) {
        console.log("ERROR: " + e.message);
    });
    req2.write(JSON.stringify(json));
    req2.end();
    res.redirect('/');
});

// PUT function
app.post('/PUT', function(req, res) {
    json = req.body;
    id = json['id'];
    // Update REST options for PUT
    options['method'] = "PUT";
    options['path'] = "/todo/" + id;
    options['headers'] = { 'content-type': 'application/json' };
    var req2 = http.request(options, function(res) {
        console.log("STATUS: " + res.statusCode);
        console.log("HEADERS: " + JSON.stringify(res.headers));
        res.setEncoding("utf8");
        res.on("data", function(chunk) {
            console.log("BODY: " + chunk);
        });
    });
    req2.on("error", function(e) {
        console.log("ERROR: " + e.message);
    });
    req2.write(JSON.stringify(json));
    req2.end();
    res.redirect('/');
});

// Handle DELETE requests
app.post('/DELETE', function(req, res) {
    option = req.body;
    id = option['id'];
    console.log(id);
    // Update REST options for DELETE
    options['method'] = "DELETE";
    options['path'] = "/todo/" + id;
    console.log(options);
    http.request(options, function(res2) {
        res2.setEncoding('utf8');
        res2.on('data', function(json_chunk) {
            json_chunk_array = json_chunk['result'];
            console.log(json_chunk_array);
        });
    }).end();
    // After delete should refresh home page
    res.redirect('/');
});

// Listen on port 3000
app.listen(3000);

// Print URL for accessing server
console.log('Server running at http://127.0.0.1:3000/')