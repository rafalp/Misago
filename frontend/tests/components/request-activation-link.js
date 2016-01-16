import assert from 'assert';
import React from 'react'; // jshint ignore:line
import misago from 'misago/index';
import { RequestLinkForm, LinkSent } from 'misago/components/request-activation-link'; // jshint ignore:line
import snackbar from 'misago/services/snackbar';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;

describe("Request Activation Link Form", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    misago._context = {
      'SETTINGS': {
        'forum_name': 'Test forum'
      },
      'SEND_ACTIVATION_API': '/test-api/send-activation/'
    };

    /* jshint ignore:start */
    testUtils.render(<RequestLinkForm />, 'test-mount');
    /* jshint ignore:end */
  });

  afterEach(function() {
    testUtils.emptyTestContainers();
    testUtils.snackbarClear(snackbar);
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

    testUtils.simulateSubmit('#test-mount form');
  });

  it("handles invalid submit", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Enter a valid email address.",
        type: 'error'
      }, "form brought error about invalid input");
      done();
    });

    testUtils.simulateChange('#test-mount input', 'loremipsum');
    testUtils.simulateSubmit('#test-mount form');
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

    testUtils.simulateChange('#test-mount input', 'lorem@ipsum.com');
    testUtils.simulateSubmit('#test-mount form');
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

    testUtils.simulateChange('#test-mount input', 'lorem@ipsum.com');
    testUtils.simulateSubmit('#test-mount form');
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

    testUtils.simulateChange('#test-mount input', 'lorem@ipsum.com');
    testUtils.simulateSubmit('#test-mount form');
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

    testUtils.simulateChange('#test-mount input', 'lorem@ipsum.com');
    testUtils.simulateSubmit('#test-mount form');

    testUtils.onElement('.page-error-banned .lead', function() {
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

    testUtils.render(<RequestLinkForm callback={callback} />, 'test-mount');
    /* jshint ignore:end */

    testUtils.simulateChange('#test-mount input', 'lorem@ipsum.com');
    testUtils.simulateSubmit('#test-mount form');
  });
});

describe("Activation Link Sent", function() {
  afterEach(function() {
    testUtils.emptyTestContainers();
  });

  it("renders message", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    let callback = function() {
      assert.ok(true, "callback function was called on button press");
      done();
    };

    testUtils.render(<LinkSent user={{email: 'bob@boberson.com' }} callback={callback} />, 'test-mount');
    /* jshint ignore:end */

    let element = $('#test-mount .well-done');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('p').text().trim(),
      "Activation link was sent to bob@boberson.com",
      "component renders valid message");

    testUtils.simulateClick('#test-mount .btn-primary');
  });
});