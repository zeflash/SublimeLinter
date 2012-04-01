/*jshint boss: true, evil: true */
/*globals load quit readline lint JSHINT */

// usage:
//   jsc ${envHome}/jsc.js -- /path/to/linter/ ${lineCount} {option1:true,option2:false}

var LINTER_PATH = arguments[0].replace(/\/$/, '') + '/';
load(LINTER_PATH + 'linter.js');

if (typeof lint === 'undefined') {
    print('JSC: Could not load linter.js.');
    quit();
}

var process = function (args) {
    var opts,
        lineCount = parseInt(args[1], 10);

    if (isNaN(lineCount)) {
        print('JSC: Must provide number of lines to read from stdin.');
        quit();
    }

    try {
        opts = JSON.parse(args[2]);
    } catch (e) {
    } finally {
        if (!opts) opts = {};
    }

    var code = readline();

    for (var i = 0; i < lineCount; ++i) {
        code += '\n' + readline();
    }

    var results = lint(code, opts);

    print(JSON.stringify(results));
    quit();
};

process(arguments);
