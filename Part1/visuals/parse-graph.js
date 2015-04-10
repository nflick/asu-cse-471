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
    lineArr = lineArr.map(function(x) {
      x = +x;
      if (x === 34)
        return 0;
      else if (x === 173)
        return 1;
      else if (x === 198)
        return 2;
      else
        return x - 346;
    });

    this.push({ source: lineArr[0], target: lineArr[1] });

    next();
  }))
  .on('data', function(data) {
    output.push(data);
  })
  .on('end', function() {
    var nodes = [];

    for (var i = 0; i < 227; i++) {
      nodes.push({ index:i });
    }

    process.stdout.write(JSON.stringify({links: output, nodes: nodes}));
  });
