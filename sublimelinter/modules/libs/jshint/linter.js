/*jshint node: true */
/*globals LINTER_PATH load */

// Make JSHINT a Node module, if possible.
if (typeof exports === 'object' && exports) {
    exports.lint = lint;
    var JSHINT = require("./jshint").JSHINT;
// Otherwise load via JSC
} else {
    load(LINTER_PATH + "jshint.js");
}

function lint(code, config) {
    var results = [];

    try {
        JSHINT(code, config);
    } catch (e) {
        results.push({line: 1, character: 1, reason: e.message});
    } finally {
        JSHINT.errors.forEach(function (error) {
            if (error) {
                results.push(error);
            }
        });
    }

    return results;
}
