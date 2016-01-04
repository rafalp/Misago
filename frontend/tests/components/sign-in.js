import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import misago from 'misago/index';
import SignIn from 'misago/components/sign-in'; // jshint ignore:line
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';

let component = null;
let snackbarStore = null;

describe("Sign In", function() {
  beforeEach(function() {
    snackbarStore = window.snackbarStoreMock();
    snackbar.init(snackbarStore);
    window.initModal(modal);

    misago._context = {
      'SETTINGS': {
        forum_name: 'Test Forum'
      },

      'AUTH_API': '/test-api/auth/',
      'REQUEST_ACTIVATION_URL': '/request-activation/',
      'FORGOTTEN_PASSWORD_URL': '/forgotten-password/'
    };

    /* jshint ignore:start */
    component = ReactDOM.render(
      <SignIn />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
  });

  afterEach(function() {
    window.emptyTestContainers();
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

  it("handles empty submit", function() {
    window.simulateSubmit('#test-mount form');

    assert.deepEqual(snackbarStore.message, {
      message: "Fill out both fields.",
      type: 'error'
    }, "form validation rejected empty form");
  });

  it("handles partial submit", function() {
    window.simulateChange('#id_username', 'loremipsum');
    window.simulateSubmit('#test-mount form');

    assert.deepEqual(snackbarStore.message, {
      message: "Fill out both fields.",
      type: 'error'
    }, "form validation rejected empty form");
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: '/test-api/auth/',
      status: 500
    });

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_password', 'pass1234');
    window.simulateSubmit('#test-mount form');

    window.afterAjax(component, function() {
      assert.deepEqual(snackbarStore.message, {
        message: "Unknown error has occured.",
        type: 'error'
      }, "form raised alert about backend error");
      done();
    });
  });

  it("handles invalid credentials", function(done) {
    let message = 'Login or password is incorrect.';

    $.mockjax({
      url: '/test-api/auth/',
      status: 400,
      responseText: {
        'detail': message,
        'code': 'invalid_login'
      }
    });

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_password', 'pass1234');
    window.simulateSubmit('#test-mount form');

    window.afterAjax(component, function() {
      assert.deepEqual(snackbarStore.message, {
        message: message,
        type: 'error'
      }, "form raised alert about invalid credentials");
      done();
    });
  });

  it("to admin-activated account", function(done) {
    let message = "This account has to be activated by admin.";

    $.mockjax({
      url: '/test-api/auth/',
      status: 400,
      responseText: {
        'detail': message,
        'code': 'inactive_admin'
      }
    });

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_password', 'pass1234');
    window.simulateSubmit('#test-mount form');

    window.afterAjax(component, function() {
      assert.deepEqual(snackbarStore.message, {
        message: message,
        type: 'info'
      }, "form raised alert about admin-activated account");
      done();
    });
  });

  it("to user-activated account", function(done) {
    let message = "This account has to be activated.";

    $.mockjax({
      url: '/test-api/auth/',
      status: 400,
      responseText: {
        'detail': message,
        'code': 'inactive_user'
      }
    });

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_password', 'pass1234');
    window.simulateSubmit('#test-mount form');

    window.afterAjax(component, function() {
      assert.deepEqual(snackbarStore.message, {
        message: message,
        type: 'info'
      }, "form raised alert about user-activated account");

      let activateButton = $('#test-mount .modal-footer .btn-success');
      assert.ok(activateButton.length, "activation button displayed");
      assert.equal(
        activateButton.attr('href'), misago.get('REQUEST_ACTIVATION_URL'),
        "button to activation form has valid url");

      done();
    });
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

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_password', 'pass1234');
    window.simulateSubmit('#test-mount form');

    window.onElement('.page-error-banned .lead', function() {
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

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_password', 'pass1234');
    window.simulateSubmit('#test-mount form');

    window.onElement('.page-error-banned .lead', function() {
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

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_password', 'pass1234');
    window.simulateSubmit('#test-mount form');
  });
});