import assert from 'assert';
import React from 'react'; // jshint ignore:line
import misago from 'misago/index';
import { ResetPasswordForm, PasswordChangedPage } from 'misago/components/reset-password-form'; // jshint ignore:line
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;

describe("Reset Password Form", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    misago._context = {
      'SETTINGS': {
        'forum_name': 'Test forum',
        'password_length_min': 4
      },
      'CHANGE_PASSWORD_API': '/test-api/change-password/1/s0m3-t0k3n/'
    };

    /* jshint ignore:start */
    testUtils.render(<ResetPasswordForm />, 'test-mount');
    /* jshint ignore:end */
  });

  afterEach(function() {
    testUtils.emptyTestContainers();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function() {
    let element = $('#test-mount .well-form-reset-password');
    assert.ok(element.length, "component renders");
  });

  it("handles empty submit", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Enter new password.",
        type: 'error'
      }, "form brought error about no input");
      done();
    });

    testUtils.simulateSubmit('#test-mount form');
  });

  it("handles invalid submit", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Valid password must be at least 4 characters long.",
        type: 'error'
      }, "form brought error about invalid input");
      done();
    });

    testUtils.simulateChange('#test-mount input', 'abc');
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
      url: '/test-api/change-password/1/s0m3-t0k3n/',
      status: 500
    });

    testUtils.simulateChange('#test-mount input', 'Som3L33tP455');
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
      url: '/test-api/change-password/1/s0m3-t0k3n/',
      status: 400,
      responseText: {
        detail: "Nope nope nope!"
      }
    });

    testUtils.simulateChange('#test-mount input', 'Som3L33tP455');
    testUtils.simulateSubmit('#test-mount form');
  });

  it("from banned IP", function(done) {
    $.mockjax({
      url: '/test-api/change-password/1/s0m3-t0k3n/',
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

    testUtils.simulateChange('#test-mount input', 'Som3L33tP455');
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
      url: '/test-api/change-password/1/s0m3-t0k3n/',
      status: 200,
      responseText: {
        'username': 'Bob'
      }
    });

    /* jshint ignore:start */
    let callback = function(apiResponse) {
      assert.deepEqual(apiResponse, {
        'username': 'Bob'
      }, "callback function was called on ajax success");
      done();
    };

    testUtils.render(<ResetPasswordForm callback={callback} />, 'test-mount');
    /* jshint ignore:end */

    testUtils.simulateChange('#test-mount input', 'Som3L33tP455');
    testUtils.simulateSubmit('#test-mount form');
  });
});

describe("Password Changed Page", function() {
  beforeEach(function() {
    testUtils.initModal(modal);

    misago._context = {
      'FORGOTTEN_PASSWORD_URL': '/forgotten-password/'
    };

    /* jshint ignore:start */
    testUtils.render(<PasswordChangedPage user={{username: 'BobBoberson'}} />, 'test-mount');
    /* jshint ignore:end */
  });

  afterEach(function() {
    testUtils.emptyTestContainers();
  });

  it("renders", function() {
    let element = $('#test-mount .page-forgotten-password-changed');
    assert.ok(element.length, "component renders");

    assert.equal(
      $('#test-mount .page .message-body p.lead').text().trim(),
      "BobBoberson, your password has been changed successfully.",
      "displayed password changed page with valid message.");
  });

  it('opens sign in modal on click', function(done) {
    testUtils.simulateClick('#test-mount .btn-primary');

    testUtils.onElement('#modal-mount .modal-sign-in', function() {
      assert.ok(true, "sign in modal was displayed");
      done();
    });
  });
});