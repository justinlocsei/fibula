#!/usr/bin/env node

var fs = require('fs');
var path = require('path');

var _ = require('lodash');
var pad = require('pad');
var request = require('request');
var yargs = require('yargs');

// Metrics on the current pass
var CONCURRENCY = 0;
var RUNNING_REQUESTS = 0;
var SAMPLE_START = null;
var SAMPLE_END = null;

// Containers for pass and request data
var REQUESTS = [];
var PASSES = [];

// Load the benchmark based on the user's input
var BENCHMARK = determineBenchmark();
var MAX_REQUESTS = BENCHMARK.requests;
var MAX_CONCURRENCY = BENCHMARK.maxConcurrency;

// Run the benchmark
runBenchmark();

/**
 * Determine the current benchmark to run from the command-line options
 *
 * @returns {object}
 */
function determineBenchmark() {
  var options = yargs
    .option('host', {
      default: null,
      describe: 'The hostname to benchmark'
    })
    .option('protocol', {
      default: 'https',
      describe: 'The protocol to use'
    })
    .option('service', {
      default: null,
      describe: 'The name of the service to benchmark'
    })
    .argv;

  if (!options.host || !options.service) {
    console.log('Usage: ' + path.basename(__filename) + ' --host=HOSTNAME --service=SERVICE [--protocol=PROTOCOL]');
    process.exit(1);
  }

  var manifest = JSON.parse(fs.readFileSync(path.join(__dirname, 'services.json')));
  var service = manifest.services.find(s => s.slug === options.service);

  return {
    data: service.post,
    maxConcurrency: service.concurrency,
    requests: service.requests,
    url: options.protocol + '://' + options.host + service.path
  };
}

/**
 * Enqueue all requests for the next concurrency level
 */
function runBenchmark() {
  CONCURRENCY++;
  if (CONCURRENCY > MAX_CONCURRENCY) {
    return summarizeAll();
  }

  SAMPLE_START = null;
  SAMPLE_END = null;

  console.log('Pass ' + CONCURRENCY);
  _.range(0, MAX_REQUESTS).forEach(function(i) {
    measureRequest(i);
  });
}

/**
 * Measure the duration of a request
 *
 * @param {number} index The index of a request
 */
function measureRequest(index) {
  if (RUNNING_REQUESTS >= CONCURRENCY) {
    return setTimeout(function() {
      measureRequest(index);
    }, 1);
  }

  RUNNING_REQUESTS++;

  var startTime = new Date().getTime();
  SAMPLE_START = SAMPLE_START || startTime;

  function resolveRequest(error, body) {
    RUNNING_REQUESTS--;
    var endTime = new Date().getTime();
    var duration = endTime - startTime;

    process.stdout.write('.');
    var dataIndex = CONCURRENCY - 1;
    REQUESTS[dataIndex] = REQUESTS[dataIndex] || [];
    REQUESTS[dataIndex].push(duration);
    if (REQUESTS[dataIndex].length === MAX_REQUESTS) {
      SAMPLE_END = endTime;
      summarizePass();
    }
  }

  if (BENCHMARK.data) {
    request.post(BENCHMARK.url, {
      form: BENCHMARK.data,
      rejectUnauthorized: false
    }, resolveRequest);
  } else {
    request.get(BENCHMARK.url, resolveRequest);
  }
}

/**
 * Show the results of a single benchmark pass
 */
function summarizePass() {
  var data = REQUESTS[CONCURRENCY - 1];
  var average = _.sum(data) / data.length;
  var duration = SAMPLE_END - SAMPLE_START;

  var strTime = Math.ceil(average) + 'ms';
  var strRate = Math.floor(MAX_REQUESTS / (duration / 1000)).toString();

  console.log('');
  console.log('Benchmark Duration:    ' + Math.ceil(duration) + 'ms');
  console.log('Average Response Time: ' + strTime);
  console.log('Requests per Second:   ' + strRate);
  console.log('');

  PASSES.push({
    rate: strRate,
    time: strTime
  });

  runBenchmark();
}

/**
 * Show aggregate data from all PASSES
 */
function summarizeAll() {
  var labels = ['Concurrency', 'Response Time', 'Requests per Second'];
  var separator = ' | ';

  var data = PASSES.map(function(pass, i) {
    return [
      (i + 1).toString(),
      pass.time,
      pass.rate
    ];
  });

  var headerRow = labels.join(separator);
  console.log(headerRow);
  console.log(Array(headerRow.length + 1).join('-'));

  data.forEach(function(datum) {
    datum.forEach(function(value, j) {
      var ender = j === datum.length - 1 ? '' : separator;
      process.stdout.write(pad(value, labels[j].length) + ender);
    });
    console.log('');
  });

  console.log(Array(headerRow.length + 1).join('-'));
  var rpsValues = data.map(d => parseInt(d[2], 10));
  console.log('Requests per minute: ' + Math.floor(_.sum(rpsValues) / rpsValues.length) * 60);
}
