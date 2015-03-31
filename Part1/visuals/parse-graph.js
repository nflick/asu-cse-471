var path = require('path'),
    fs = require('fs'),
    split = require('split'),
    through = require('through2');

var output = [];

process.stdin
  .pipe(split())
  .pipe(through.obj(function(buf, _, next) {
    var line = buf.toString();
    if (line.length === 0) return next();

    var lineArr = line.split(' ');

    this.push({ from: lineArr[0], to: lineArr[1] });

    next();
  }))
  .on('data', function(data) {
    output.push(data);
  })
  .on('end', function() {
    process.stdout.write(JSON.stringify(output));
  });
