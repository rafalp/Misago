(function () {
  'use strict';

  var app = null;

  QUnit.acceptance("Sign In", {
    beforeEach: function() {
      $('#hidden-login-form').on('submit.stopInTest', function(event) {
        event.stopPropagation();
        return false;
      });
      app = initTestMisago();
      app.context.AUTH_API = '/test-api/auth/';
    },
    afterEach: function() {
      $('#hidden-login-form').off('submit.stopInTest');
      app.destroy();
    }
  });

  QUnit.test('with empty credentials', function(assert) {
    var done = assert.async();

    app.modal('sign-in');

    waitForElement('.modal-signin');
    click('.modal-signin .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Fill out both fields.",
        "login form raised alert about empty inputs.");
      done();
    });
  });

  QUnit.test('with backend error', function(assert) {
    $.mockjax({
      url: '/test-api/auth/',
      status: 500
    });

    var done = assert.async();

    app.modal('sign-in');

    waitForElement('.modal-signin');
    fillIn('.modal-signin .form-group:first-child input', 'SomeFake');
    fillIn('.modal-signin .form-group:last-child input', 'pass1234');
    click('.modal-signin .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Unknown error has occured.",
        "login form raised alert about backend error.");
      done();
    });
  });

  QUnit.test('with invalid credentials', function(assert) {
    var message = 'Login or password is incorrect.';
    $.mockjax({
      url: '/test-api/auth/',
      status: 400,
      responseText: {
        'detail': message,
        'code': 'invalid_login'
      }
    });

    var done = assert.async();

    app.modal('sign-in');

    waitForElement('.modal-signin');
    fillIn('.modal-signin .form-group:first-child input', 'SomeFake');
    fillIn('.modal-signin .form-group:last-child input', 'pass1234');
    click('.modal-signin .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), message,
        "login form raised alert about invalid credentials.");
      done();
    });
  });

  QUnit.test('to admin-activated account', function(assert) {
    var message = "This account has to be activated by admin.";
    $.mockjax({
      url: '/test-api/auth/',
      status: 400,
      responseText: {
        'detail': message,
        'code': 'inactive_admin'
      }
    });

    var done = assert.async();

    app.modal('sign-in');

    waitForElement('.modal-signin');
    fillIn('.modal-signin .form-group:first-child input', 'SomeFake');
    fillIn('.modal-signin .form-group:last-child input', 'pass1234');
    click('.modal-signin .btn-primary');

    onElement('.alerts .alert-info', function() {
      assert.equal(getAlertMessage(), message,
        "login form raised alert about admin-activated account.");
      done();
    });
  });

  QUnit.test('to user-activated account', function(assert) {
    var message = "This account has to be activated.";
    $.mockjax({
      url: '/test-api/auth/',
      status: 400,
      responseText: {
        'detail': message,
        'code': 'inactive_user'
      }
    });

    var doneAlert = assert.async();
    var doneBtn = assert.async();

    app.modal('sign-in');

    waitForElement('.modal-signin');
    fillIn('.modal-signin .form-group:first-child input', 'SomeFake');
    fillIn('.modal-signin .form-group:last-child input', 'pass1234');
    click('.modal-signin .btn-primary');

    onElement('.alerts .alert-info', function() {
      assert.equal(getAlertMessage(), message,
        "login form raised alert about admin-activated account.");
      doneAlert();
    });

    onElement('.modal-signin .btn-success', function() {
      assert.ok(true, "login form displayed account activation button.");
      doneBtn();
    });
  });

  QUnit.test('from banned ip', function(assert) {
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

    var done = assert.async();

    app.modal('sign-in');

    waitForElement('.modal-signin');
    fillIn('.modal-signin .form-group:first-child input', 'SomeFake');
    fillIn('.modal-signin .form-group:last-child input', 'pass1234');
    click('.modal-signin .btn-primary');

    onElement('.page-error-banned .lead', function() {
      assert.equal(
        getElementText('.page .message-body .lead'),
        "Your ip is banned for spamming.",
        "login form displayed error banned page with ban message.");

      waitForElementRemoval('.modal-signin');
      then(function() {
        assert.ok(true, "signin modal was closed.");
        done();
      });
    });
  });

  QUnit.test('to banned account', function(assert) {
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

    var done = assert.async();

    app.modal('sign-in');

    waitForElement('.modal-signin');
    fillIn('.modal-signin .form-group:first-child input', 'SomeFake');
    fillIn('.modal-signin .form-group:last-child input', 'pass1234');
    click('.modal-signin .btn-primary');

    onElement('.page-error-banned .lead', function() {
      assert.equal(
        getElementText('.page .message-body .lead'),
        "You are banned for trolling.",
        "login form displayed error banned page with ban message.");

      waitForElementRemoval('.modal-signin');
      then(function() {
        assert.ok(true, "signin modal was closed.");
        done();
      });
    });
  });

  QUnit.test('success', function(assert) {
    $.mockjax({
      url: '/test-api/auth/',
      status: 200,
      responseText: {
        'detail': 'ok'
      }
    });

    var done = assert.async();

    app.modal('sign-in');

    waitForElement('.modal-signin');
    fillIn('.modal-signin .form-group:first-child input', 'SomeFake');
    fillIn('.modal-signin .form-group:last-child input', 'pass1234');
    click('.modal-signin .btn-primary');

    var $form = $('#hidden-login-form');
    $form.on('submit.stopInTest', function(event) {
      event.stopPropagation();
      assert.ok(true, 'login form was submit');
      assert.equal($form.find('input[name="username"]').val(), 'SomeFake',
        "hidden form was filled with valid username.");
      assert.equal($form.find('input[name="password"]').val(), 'pass1234',
        "hidden form was filled with valid password.");
      done();
      return false;
    });
  });
}());
