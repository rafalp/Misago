(function () {
  'use strict';

  var app = null;

  QUnit.acceptance("Reset Forgotten Password", {
    beforeEach: function() {
      app = initTestMisago();
      app.context.CHANGE_PASSWORD_API = '/test-api/auth/change-password/';

      var mount = document.getElementById('component-mount');
      m.mount(mount, app.component('forgotten-password:reset-password'));
    },
    afterEach: function() {
      app.destroy();
    }
  });

  QUnit.test('submit empty form', function(assert) {
    var done = assert.async();

    click('#component-mount .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Enter new password.",
        "form raised alert about empty input.");
      done();
    });
  });

  QUnit.test('submit too short password', function(assert) {
    var done = assert.async();

    fillIn('#component-mount input[type="password"]', 'no');
    click('#component-mount .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(
        getAlertMessage(),
        "Valid password must be at least 5 characters long.",
        "form raised alert about invalid new password.");
      done();
    });
  });

  QUnit.test('with backend banned', function(assert) {
    $.mockjax({
      url: app.context.CHANGE_PASSWORD_API,
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

    fillIn('#component-mount input[type="password"]', 'L0r3m1p5um');
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
    var message = "Some evil rejection happened!";
    $.mockjax({
      url: app.context.CHANGE_PASSWORD_API,
      status: 400,
      responseText: {
        'detail': message
      }
    });

    var done = assert.async();

    fillIn('#component-mount input[type="password"]', 'L0r3m1p5um');
    click('#component-mount .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), message,
        "reset password form raised alert returned by backend.");
      done();
    });
  });

  QUnit.test('with success', function(assert) {
    $.mockjax({
      url: app.context.CHANGE_PASSWORD_API,
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    var done = assert.async();

    fillIn('#component-mount input[type="password"]', 'L0r3m1p5um');
    click('#component-mount .btn-primary');

    onElement('.page-forgotten-password-done .message-body p', function() {
      assert.equal(
        getElementText('.message-body p.lead'),
        "Bob, your password has been changed successfully.",
        "reset form displayed success page.");
      done();
    });
  });
}());
