(function () {
  'use strict';

  var app = null;

  QUnit.acceptance("Request Change Password E-mail", {
    beforeEach: function() {
      app = initTestMisago();
      app.context.SEND_PASSWORD_RESET_API = '/test-api/auth/send-password-form/';

      var mount = document.getElementById('component-mount');
      m.mount(mount, app.component('forgotten-password:request-link'));
    },
    afterEach: function() {
      app.destroy();
    }
  });

  QUnit.test('submit empty form', function(assert) {
    var done = assert.async();

    click('#component-mount .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Enter a valid email address.",
        "form raised alert about empty input.");
      done();
    });
  });

  QUnit.test('submit invalid form', function(assert) {
    var done = assert.async();

    fillIn('#component-mount input[type="text"]', 'not-an-email!');
    click('#component-mount .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Enter a valid email address.",
        "form raised alert about invalid input.");
      done();
    });
  });

  QUnit.test('with backend banned', function(assert) {
    $.mockjax({
      url: '/test-api/auth/send-password-form/',
      status: 403,
      responseText: {
        'ban': {
          'expires_on': null,
          'message': {
            'plain': 'This is test ban.',
            'html': '<p>This is test ban.</p>'
          }
        }
      }
    });

    var done = assert.async();

    fillIn('#component-mount input[type="text"]', 'valid@email.com');
    click('#component-mount .btn-primary');

    onElement('.page-error-banned .message-body', function() {
      assert.ok(true, "Permission denied error page was displayed.");
      assert.equal(
        getElementText('.page .message-body .lead'),
        "This is test ban.",
        "Banned page displayed ban message.");
      done();
    });
  });

  QUnit.test('with backend error', function(assert) {
    var message = "No user found for email!";
    $.mockjax({
      url: '/test-api/auth/send-password-form/',
      status: 400,
      responseText: {
        'detail': message
      }
    });

    var done = assert.async();

    fillIn('#component-mount input[type="text"]', 'valid@email.com');
    click('#component-mount .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), message,
        "request form raised alert returned by backend.");
      done();
    });
  });

  QUnit.test('without admin activation', function(assert) {
    var message = "Your account needs admin activation!";
    $.mockjax({
      url: '/test-api/auth/send-password-form/',
      status: 400,
      responseText: {
        'code': 'inactive_admin',
        'detail': message
      }
    });

    var done = assert.async();

    fillIn('#component-mount input[type="text"]', 'valid@email.com');
    click('#component-mount .btn-primary');

    onElement('.message-body p', function() {
      assert.equal(
        getElementText('.message-body p:nth-child(2)'), message,
        "request form displayed admin activation message.");
      done();
    });
  });

  QUnit.test('without user activation', function(assert) {
    var message = "Your account needs admin activation!";
    $.mockjax({
      url: '/test-api/auth/send-password-form/',
      status: 400,
      responseText: {
        'code': 'inactive_admin',
        'detail': message
      }
    });

    var done = assert.async();

    fillIn('#component-mount input[type="text"]', 'valid@email.com');
    click('#component-mount .btn-primary');

    onElement('.message-body p', function() {
      assert.equal(
        getElementText('.message-body p:nth-child(2)'), message,
        "request form displayed user activation message.");
      done();
    });
  });

  QUnit.test('with success', function(assert) {
    $.mockjax({
      url: '/test-api/auth/send-password-form/',
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    var done = assert.async();

    fillIn('#component-mount input[type="text"]', 'valid@email.com');
    click('#component-mount .btn-primary');

    onElement('.well-done .message-body p', function() {
      assert.equal(
        getElementText('.message-body p'),
        "Reset password link sent to bob@boberson.com.",
        "request form displayed success message.");
      done();
    });
  });

  QUnit.test('reset', function(assert) {
    $.mockjax({
      url: '/test-api/auth/send-password-form/',
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    var done = assert.async();

    fillIn('#component-mount input[type="text"]', 'valid@email.com');
    click('#component-mount .btn-primary');
    click('#component-mount .btn-default');

    onElement('.well-form', function() {
      assert.ok(true, 'reset button reset component state.');
      done();
    });
  });
}());
