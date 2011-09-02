/*jshint boss: true */

// usage:
//   jsc ${env_home}/jsc.js -- ${file} ${lines} "{option1:true,option2:false} ${env_home}"
var env_home = '';
if (arguments.length > 3) {
  env_home = arguments[3].toString().replace(/\/env$/, '/');
}
load(env_home + "jshint.js");

if (typeof(JSHINT) === 'undefined') {
  print('jshint: Could not load jshint.js, tried "' + env_home + 'jshint.js".');
  quit();
}

(function(args){
    var home  = args[3],
        name  = args[0],
        lines = eval(args[1]),
        opts  = (function(arg){
            switch (arg) {
            case undefined:
            case '':
                return {};
            default:
                return eval('(' + arg + ')');
            }
        })(args[2]);
    

    if (!name) {
        print('jshint: No file name was provided.');
        quit();
    }

    if (!lines) {
        print('jshint: Must provide number of lines to read from stdin.');
        quit();
    }

    var input = '';
    var _input, cnt = 0;
    while(++cnt < lines && (_input = readline()) !== null) {
        if (input) {
            input = input + '\n';
        }
        input = input + _input;
    }
    //print('>>>>',input,'<<<<');

    var results = [];
    if (!JSHINT(input, opts)) {
        for (var i = 0, err; err = JSHINT.errors[i]; i++) {
            results.push(err);
        }
    }

    print(JSON.stringify(results));
    quit();
})(arguments);