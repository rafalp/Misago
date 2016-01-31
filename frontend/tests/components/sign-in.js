import assert from 'assert';
import React from 'react'; // jshint ignore:line
import misago from 'misago/index';
import SignIn from 'misago/components/sign-in'; // jshint ignore:line
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;

describe("Sign In", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);
    testUtils.initModal(modal);
    testUtils.initEmptyStore(store);

    misago._context = {
      'SETTINGS': {
        forum_name: 'Test Forum'
      },

      'AUTH_API': '/test-api/auth/',
      'REQUEST_ACTIVATION_URL': '/request-activation/',
      'FORGOTTEN_PASSWORD_URL': '/forgotten-password/'
    };

    /* jshint ignore:start */
    testUtils.render(<SignIn />);
    /* jshint ignore:end */
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function() {
    assert.ok($('#test-mount .modal-sign-in #id_username').length,
      "username input rendered");
    assert.ok($('#test-mount .modal-sign-in #id_password').length,
      "password input rendered");

    assert.equal(
      $('#test-mount .modal-footer .btn-default').attr('href'),
      misago.get('FORGOTTEN_PASSWORD_URL'),
      "forgotten password form url is valid");
  });

  it("handles empty submit", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Fill out both fields.",
        type: 'error'
      }, "form validation rejected empty form");
      done();
    });

    testUtils.simulateSubmit('#test-mount form');
  });

  it("handles partial submit", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Fill out both fields.",
        type: 'error'
      }, "form validation rejected empty form");
      done();
    });

    testUtils.simulateChange('#id_username', 'loremipsum');
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
      url: '/test-api/auth/',
      status: 500
    });

    testUtils.simulateChange('#id_username', 'SomeFake');
    testUtils.simulateChange('#id_password', 'pass1234');
    testUtils.simulateSubmit('#test-mount form');
  });

  it("handles invalid credentials", function(done) {
    let testMessage = 'Login or password is incorrect.';

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: testMessage,
        type: 'error'
      }, "form raised alert about invalid credentials");
      done();
    });

    $.mockjax({
      url: '/test-api/auth/',
      status: 400,
      responseText: {
        'detail': testMessage,
        'code': 'invalid_login'
      }
    });

    testUtils.simulateChange('#id_username', 'SomeFake');
    testUtils.simulateChange('#id_password', 'pass1234');
    testUtils.simulateSubmit('#test-mount form');
  });

  it("to admin-activated account", function(done) {
    let testMessage = "This account has to be activated by admin.";

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: testMessage,
        type: 'info'
      }, "form raised alert about admin-activated account");
      done();
    });

    $.mockjax({
      url: '/test-api/auth/',
      status: 400,
      responseText: {
        'detail': testMessage,
        'code': 'inactive_admin'
      }
    });

    testUtils.simulateChange('#id_username', 'SomeFake');
    testUtils.simulateChange('#id_password', 'pass1234');
    testUtils.simulateSubmit('#test-mount form');
  });

  it("to user-activated account", function(done) {
    let testMessage = "This account has to be activated.";

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: testMessage,
        type: 'info'
      }, "form raised alert about user-activated account");

      let activateButton = $('#test-mount .modal-footer .btn-success');
      assert.ok(activateButton.length, "activation button displayed");
      assert.equal(
        activateButton.attr('href'), misago.get('REQUEST_ACTIVATION_URL'),
        "button to activation form has valid url");

      done();
    });

    $.mockjax({
      url: '/test-api/auth/',
      status: 400,
      responseText: {
        'detail': testMessage,
        'code': 'inactive_user'
      }
    });

    testUtils.simulateChange('#id_username', 'SomeFake');
    testUtils.simulateChange('#id_password', 'pass1234');
    testUtils.simulateSubmit('#test-mount form');
  });

  it("from banned IP", function(done) {
    $.mockjax({
      url: '/test-api/auth/',
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

    testUtils.simulateChange('#id_username', 'SomeFake');
    testUtils.simulateChange('#id_password', 'pass1234');
    testUtils.simulateSubmit('#test-mount form');

    testUtils.onElement('.page-error-banned .lead', function() {
      assert.equal(
        $('.page .message-body .lead p').text().trim(),
        "Your ip is banned for spamming.",
        "displayed error banned page with ban message.");

      done();
    });
  });

  it("to banned account", function(done) {
    $.mockjax({
      url: '/test-api/auth/',
      status: 400,
      responseText: {
        'detail': {
          'expires_on': null,
          'message': {
            'plain': 'You are banned for trolling.',
            'html': '<p>You are banned for trolling.</p>',
          }
        },
        'code': 'banned'
      }
    });

    testUtils.simulateChange('#id_username', 'SomeFake');
    testUtils.simulateChange('#id_password', 'pass1234');
    testUtils.simulateSubmit('#test-mount form');

    testUtils.onElement('.page-error-banned .lead', function() {
      assert.equal(
        $('.page .message-body .lead p').text().trim(),
        "You are banned for trolling.",
        "displayed error banned page with ban message.");

      done();
    });
  });

  it("login successfully", function(done) {
    $('body').append('<div id="hidden-login-form"></div>');

    $.mockjax({
      url: '/test-api/auth/',
      status: 200,
      responseText: {
        'detail': 'ok'
      }
    });

    let form = $('#hidden-login-form');
    form.on('submit', function(e) {
      e.stopPropagation();

      assert.equal(form.find('input[name="username"]').val(), 'SomeFake',
        "form was filled with valid username.");
      assert.equal(form.find('input[name="password"]').val(), 'pass1234',
        "form was filled with valid password.");

      form.remove();
      done();

      return false;
    });

    testUtils.simulateChange('#id_username', 'SomeFake');
    testUtils.simulateChange('#id_password', 'pass1234');
    testUtils.simulateSubmit('#test-mount form');
  });
});