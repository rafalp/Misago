import assert from 'assert';
import React from 'react'; // jshint ignore:line
import misago from 'misago/index';
import { RequestResetForm, LinkSent, AccountInactivePage } from 'misago/components/request-password-reset'; // jshint ignore:line
import snackbar from 'misago/services/snackbar';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;

describe("Request Password Reset Form", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    misago._context = {
      'SETTINGS': {
        'forum_name': 'Test forum'
      },
      'SEND_PASSWORD_RESET_API': '/test-api/request-password-reset/'
    };

    /* jshint ignore:start */
    testUtils.render(<RequestResetForm />);
    /* jshint ignore:end */
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function() {
    let element = $('#test-mount .well-form-request-password-reset');
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
      url: '/test-api/request-password-reset/',
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
      url: '/test-api/request-password-reset/',
      status: 400,
      responseText: {
        detail: "Nope nope nope!"
      }
    });

    testUtils.simulateChange('#test-mount input', 'lorem@ipsum.com');
    testUtils.simulateSubmit('#test-mount form');
  });

  it("displays activation required message", function(done) { // jshint ignore:line
    $.mockjax({
      url: '/test-api/request-password-reset/',
      status: 400,
      responseText: {
        code: 'inactive_user',
        detail: "Your account is inactive!"
      }
    });

    /* jshint ignore:start */
    let showInactivePage = function(apiResponse) {
      assert.deepEqual({
        code: apiResponse.code,
        detail: apiResponse.detail
      }, {
        code: 'inactive_user',
        detail: "Your account is inactive!"
      }, "component calls inactive page callback");

      done();
    };

    testUtils.render(<RequestResetForm showInactivePage={showInactivePage} />);
    /* jshint ignore:end */

    testUtils.simulateChange('#test-mount input', 'lorem@ipsum.com');
    testUtils.simulateSubmit('#test-mount form');
  });

  it("from banned IP", function(done) {
    $.mockjax({
      url: '/test-api/request-password-reset/',
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
      url: '/test-api/request-password-reset/',
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

    testUtils.render(<RequestResetForm callback={callback} />);
    /* jshint ignore:end */

    testUtils.simulateChange('#test-mount input', 'lorem@ipsum.com');
    testUtils.simulateSubmit('#test-mount form');
  });
});

describe("Reset Link Sent", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders message", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    let callback = function() {
      assert.ok(true, "callback function was called on button press");
      done();
    };

    testUtils.render(
      <LinkSent user={{email: 'bob@boberson.com' }}
                callback={callback} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .well-done');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('p').text().trim(),
      "Reset password link was sent to bob@boberson.com",
      "component renders valid message");

    testUtils.simulateClick('#test-mount .btn-primary');
  });
});

describe("Account Inactive Page", function() {
  beforeEach(function() {
    misago._context = {
      'REQUEST_ACTIVATION_URL': '/activate-thy-account/'
    };
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders page for user-activated user", function() {
    /* jshint ignore:start */
    testUtils.render(
      <AccountInactivePage activation='inactive_user'
                           message="Lorem ipsum dolor met." />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .page-forgotten-password-inactive');
    assert.ok(element.length, "component renders");

    assert.equal(
      $('#test-mount .page .message-body p:eq(1)').text().trim(),
      "Lorem ipsum dolor met.",
      "displayed error inactive page with backend message.");

    assert.equal($('#test-mount a').attr('href'), '/activate-thy-account/',
      "activate account link is displayed on inactive error page");
  });

  it("renders page for admin-activated user", function() {
    /* jshint ignore:start */
    testUtils.render(
      <AccountInactivePage activation='inactive_admin'
                           message="Lorem ipsum dolor met admin." />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .page-forgotten-password-inactive');
    assert.ok(element.length, "component renders");

    assert.equal(
      $('#test-mount .page .message-body p:eq(1)').text().trim(),
      "Lorem ipsum dolor met admin.",
      "displayed error inactive page with backend message.");

    assert.ok(!$('#test-mount a').length,
      "activate account link is not displayed on admin-activated error page");
  });
});