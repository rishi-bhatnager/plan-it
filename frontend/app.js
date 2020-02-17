'use strict';

/*const express = require('express');
const app = express();
const script = require('./script');

app.use('script', script);
app.get('/', function (req, res) {
  res.send("This is the '/' route in main_app");
});
/*app.get('/', (req, res) => {
  res
    .status(200)
    .send(app.js)
    .end();
});*/



var express = require('express'),
    path = require('path'),
    app = express();

app.get('/index.html',function(req,res){
   res.sendFile(path.join(__dirname + '/index.html'));
});

app.get('/styles.css',function(req,res){
    res.sendFile(path.join(__dirname + '/styles.css'));
});

app.get('/script.js',function(req,res){
    res.sendFile(path.join(__dirname + '/script.js'));
});

app.get('/', function(req, res) {
    res.redirect('index.html');
});


/*app.get('/', (req, res) => {
  res
    .status(200)
    .send('Current wife: Natacha\'s asshole!')
    .end();
});*/



// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});
// [END gae_node_request_example]

module.exports = app;
