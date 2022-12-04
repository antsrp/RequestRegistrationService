const http = require('http');
const path = require('path');
const fs = require('fs');

var CONFIG_FRONT = require('./configs/config.json')
var CONFIG_BACK = require('./configs/config_backend.json')

const host = CONFIG_FRONT.host
const port = CONFIG_FRONT.port

const extensions = {
  ".html" : "text/html",
  ".css" : "text/css",
  ".js" : "application/javascript"
};

function sendToBackend(data){
  const options = {
  hostname: CONFIG_BACK.host,
  port: CONFIG_BACK.port,
  path: CONFIG_BACK.endpoint,
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
    }
  }
  const req = http
  .request(options, res => {
    let data = ''

    res.on('data', chunk => {
      data += chunk
    })
  })
  .on('error', err => {
    console.log('Error: ', err.message)
  })

  req.write(data)
  req.end()
}

function getFile(res, filePath, mimeType){
  fs.exists(filePath,function(exists){
    if(exists){
      fs.readFile(filePath,function(err,contents){
        if(!err){
          res.writeHead(200,{
            "Content-type" : mimeType,
            "Content-Length" : contents.length
          });
          res.end(contents);
        } else {
          console.dir(err);
        };
      });
    } else {
      print404(res)
    };
  });
};

const print404 = function(res){
  res.setHeader("Content-Type", "text/plain");
  res.write(`File not found!`)
  res.end();
}

const openHTML = function(res, file){
  let path = __dirname + file
  fs.promises.readFile(path)
        .then(contents => {
            res.setHeader("Content-Type", "text/html");
            res.statusCode = 200;
            res.write(contents);
            res.end();
        })
        .catch(err => {
            res.writeHead(500);
            res.end(err);
            return;
        });
}

const requestListener = function (req, res) {
  switch(req.url){
  case "/":
    openHTML(res, "/static/html/index.html")
    break
  case "/send":
    let data = []
    req.on('data', chunk => {
      data.push(chunk)
    })
    req.on('end', () => {
      b = Buffer.concat(data)
      if(!b){
        res.statusCode = 422;
        res.write("error");
        res.end();
        return
      } 
      sendToBackend(b)
      res.statusCode = 200;
      res.write("success");
      res.end();
    })
    break
  case "/success":
    openHTML(res, "/static/html/success.html")
    break
  default:
    ext = path.extname(req.url)
    type = extensions[ext]

    if(!type) print404(res) 
    else getFile(res, __dirname + req.url, type)
  }
};

const server = http.createServer(requestListener)


server.listen(port, host, () => {
  console.log(`Server running at http://${host}:${port}/`);
});