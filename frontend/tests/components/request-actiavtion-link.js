import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import misago from 'misago/index';
import { RequestLinkForm, LinkSent } from 'misago/components/request-activation-link'; // jshint ignore:line
import snackbar from 'misago/services/snackbar';

let snackbarStore = null;

describe("Request Activation Link Form", function() {
  beforeEach(function() {
    snackbarStore = window.snackbarStoreMock();
    snackbar.init(snackbarStore);

    misago._context = {
      'SETTINGS': {
        'forum_name': 'Test forum'
      },
      'SEND_ACTIVATION_API': '/test-api/send-activation/'
    };

    /* jshint ignore:start */
    ReactDOM.render(
      <RequestLinkForm />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
  });

  afterEach(function() {
    window.emptyTestContainers();
    window.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function() {
    let element = $('#test-mount .well-form-request-activation-link');
    assert.ok(element.length, "component renders");
  });

  it("handles empty submit", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Enter a valid email address.",
        type: 'error'
      }, "form brought error about no input");
      done();
    });

    window.simulateSubmit('#test-mount form');
  });

  it("handles invalid submit", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Enter a valid email address.",
        type: 'error'
      }, "form brought error about invalid input");
      done();
    });

    window.simulateChange('#test-mount input', 'loremipsum');
    window.simulateSubmit('#test-mount form');
  });

  it("handles backend error", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Unknown error has occured.",
        type: 'error'
      }, "form raised alert about backend error");
      done();
    });

    $.mockjax({
      url: '/test-api/send-activation/',
      status: 500
    });

    window.simulateChange('#test-mount input', 'lorem@ipsum.com');
    window.simulateSubmit('#test-mount form');
  });

  it("handles backend rejection", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Nope nope nope!",
        type: 'error'
      }, "form raised alert about backend rejection");
      done();
    });

    $.mockjax({
      url: '/test-api/send-activation/',
      status: 400,
      responseText: {
        detail: "Nope nope nope!"
      }
    });

    window.simulateChange('#test-mount input', 'lorem@ipsum.com');
    window.simulateSubmit('#test-mount form');
  });

  it("handles backend info", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Your account is already active!",
        type: 'info'
      }, "form raised alert about backend info");
      done();
    });

    $.mockjax({
      url: '/test-api/send-activation/',
      status: 400,
      responseText: {
        code: 'already_active',
        detail: "Your account is already active!"
      }
    });

    window.simulateChange('#test-mount input', 'lorem@ipsum.com');
    window.simulateSubmit('#test-mount form');
  });

  it("from banned IP", function(done) {
    $.mockjax({
      url: '/test-api/send-activation/',
      status: 403,
      responseText: {
        'ban': {
          'expires_on': null,
          'message': {
            'plain': 'Your ip is banned for spamming.',
            'html': '<p>Your ip is banned for spamming.</p>',
          }
        }
      }
    });

    window.simulateChange('#test-mount input', 'lorem@ipsum.com');
    window.simulateSubmit('#test-mount form');

    window.onElement('.page-error-banned .lead', function() {
      assert.equal(
        $('.page .message-body .lead p').text().trim(),
        "Your ip is banned for spamming.",
        "displayed error banned page with ban message.");

      done();
    });
  });

  it("handles success", function(done) { // jshint ignore:line
    $.mockjax({
      url: '/test-api/send-activation/',
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    /* jshint ignore:start */
    let callback = function(apiResponse) {
      assert.deepEqual(apiResponse, {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }, "callback function was called on ajax success");
      done();
    };

    ReactDOM.render(
      <RequestLinkForm callback={callback} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    window.simulateChange('#test-mount input', 'lorem@ipsum.com');
    window.simulateSubmit('#test-mount form');
  });
});

describe("Activation Link Sent", function() {
  afterEach(function() {
    window.emptyTestContainers();
  });

  it("renders message", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    let callback = function() {
      assert.ok(true, "callback function was called on button press");
      done();
    };

    ReactDOM.render(
      <LinkSent user={{email: 'bob@boberson.com' }}
                callback={callback} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount .well-done');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('p').text().trim(),
      "Activation link was sent to bob@boberson.com",
      "component renders valid message");

    window.simulateClick('#test-mount .btn-primary');
  });
});