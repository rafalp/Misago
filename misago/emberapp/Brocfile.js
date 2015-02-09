/* global require, module */

var EmberApp = require('ember-cli/lib/broccoli/ember-app');

var app = new EmberApp({
  fingerprint: {
    enabled: false
  },
  outputPaths: {
    app: {
      html: 'index.html',
      css: {
        'app': 'misago/css/misago.css'
      },
      js: 'misago/js/misago.js'
    },
    vendor: {
      css: 'misago/css/vendor.css',
      js: 'misago/js/vendor.js'
    }
  }
});

// Use `app.import` to add additional libraries to the generated
// output files.
//
// If you need to use different assets in different
// environments, specify an object as the first parameter. That
// object's keys should be the environment name and the values
// should be the asset to use in that environment.
//
// If the library that you are including contains AMD or ES6
// modules that you would like to import into your application
// please specify an object with the list of modules as keys
// along with the exports of each module as its value.

app.import('vendor/bootstrap.js');

app.import('vendor/testutils/jquery.mockjax.js', { type: 'test' });
app.import('vendor/testutils/django-js-catalog.js', { type: 'test' });
app.import('vendor/testutils/misago-preload-data.js', { type: 'test' });

module.exports = app.toTree();
