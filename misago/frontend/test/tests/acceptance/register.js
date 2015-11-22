(function () {
  'use strict';

  var app = null;

  QUnit.acceptance("Register", {
    beforeEach: function() {
      app = initTestMisago();

      app.settings.account_activation = 'none';
      app.context.USERS_API = '/test-api/users/';
    },
    afterEach: function() {
      app.destroy();
    }
  });

  QUnit.test('registration with empty credentials', function(assert) {
    var done = assert.async();

    app.modal('register');

    click('.modal-register .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Form contains errors.",
        "empty registration form failed.");
      done();
    });
  });

  QUnit.test('registration with invalid credentials', function(assert) {
    var done = assert.async();

    app.modal('register');

    waitForElement('.modal-register');
    fillIn('#id_username', '###');
    fillIn('#id_email', 'notemail');
    fillIn('#id_password', 'nah');
    click('.modal-register .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Form contains errors.",
        "invalid registration form failed.");

      assert.equal(
        getFieldFeedback('id_username'),
        "Username can only contain latin alphabet letters and digits.",
        "username field was validated.");

      assert.equal(
        getFieldFeedback('id_email'),
        "Enter a valid email address.",
        "email field was validated.");

      assert.equal(
        getFieldFeedback('id_password'),
        "Valid password must be at least 5 characters long.",
        "password field was validated.");
      done();
    });
  });

  QUnit.test('from banned ip', function(assert) {
    $.mockjax({
      url: '/test-api/users/',
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

    app.modal('register');

    waitForElement('.modal-register');
    fillIn('#id_username', 'bob');
    fillIn('#id_email', 'bob@boberson.com');
    fillIn('#id_password', 'Som3S3cureP4ss!!!');
    click('.modal-register .btn-primary');

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

  QUnit.test('registration with backend-rejected credentials', function(assert) {
    $.mockjax({
      url: '/test-api/users/',
      status: 400,
      responseText: {
        'username': [
          "That username is already taken."
        ]
      }
    });

    var done = assert.async();

    app.modal('register');

    waitForElement('.modal-register');
    fillIn('#id_username', 'bob');
    fillIn('#id_email', 'bob@boberson.com');
    fillIn('#id_password', 'Som3S3cureP4ss!!!');
    click('.modal-register .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Form contains errors.",
        "invalid registration form was rejected.");

      assert.equal(
        getFieldFeedback('id_username'),
        "That username is already taken.",
        "username rejected by backend.");
      done();
    });
  });

  QUnit.test('registration passed with active user', function(assert) {
    $.mockjax({
      url: '/test-api/users/',
      status: 200,
      responseText: {
        'activation': 'active',
        'username': "Boberson",
        'email': "bob@boberson.com",
      }
    });

    var done = assert.async();

    app.modal('register');

    waitForElement('.modal-register');
    fillIn('#id_username', 'bob');
    fillIn('#id_email', 'bob@boberson.com');
    fillIn('#id_password', 'Som3S3cureP4ss!!!');
    click('.modal-register .btn-primary');

    onElement('.modal-message', function() {
      app.runloop.stop('refresh-after-registration');

      assert.equal(
        getElementText('.modal-message .lead'),
        "Boberson, your account has been created and you were signed in.",
        "user has been registered and signed in successfully.");
      done();
    });
  });

  QUnit.test('registration passed with user activation', function(assert) {
    $.mockjax({
      url: '/test-api/users/',
      status: 200,
      responseText: {
        'activation': 'user',
        'username': "Boberson",
        'email': "bob@boberson.com",
      }
    });

    var done = assert.async();

    app.modal('register');

    waitForElement('.modal-register');
    fillIn('#id_username', 'bob');
    fillIn('#id_email', 'bob@boberson.com');
    fillIn('#id_password', 'Som3S3cureP4ss!!!');
    click('.modal-register .btn-primary');

    onElement('.modal-message', function() {
      app.runloop.stop('refresh-after-registration');

      assert.equal(
        getElementText('.modal-message .lead'),
        "Boberson, your account has been created but you need to activate it before you will be able to sign in.",
        "user has been registered and signed in successfully.");
      done();
    });
  });

  QUnit.test('registration passed with admin activation', function(assert) {
    $.mockjax({
      url: '/test-api/users/',
      status: 200,
      responseText: {
        'activation': 'admin',
        'username': "Boberson",
        'email': "bob@boberson.com",
      }
    });

    var done = assert.async();

    app.modal('register');

    waitForElement('.modal-register');
    fillIn('#id_username', 'bob');
    fillIn('#id_email', 'bob@boberson.com');
    fillIn('#id_password', 'Som3S3cureP4ss!!!');
    click('.modal-register .btn-primary');

    onElement('.modal-message', function() {
      app.runloop.stop('refresh-after-registration');

      assert.equal(
        getElementText('.modal-message .lead'),
        "Boberson, your account has been created but board administrator will have to activate it before you will be able to sign in.",
        "user has been registered and signed in successfully.");
      done();
    });
  });
}());
