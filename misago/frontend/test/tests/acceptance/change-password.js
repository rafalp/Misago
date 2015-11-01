(function () {
  'use strict';

  var app = null;

  QUnit.acceptance("Change Password", {
    beforeEach: function() {
      app = initTestMisago();
    },
    afterEach: function() {
      app.destroy();
    }
  });

  QUnit.test('with backend banned', function(assert) {
    $.mockjax({
      url: '/test-api/auth/change-password/123/som3token/',
      status: 403,
      responseText: {
        'detail': 'You are banned!',
        'ban': {
          'expires_on': null,
          'message': {
            'plain': 'This is test ban.',
            'html': '<p>This is test ban.</p>'
          }
        }
      }
    });

    app.router.route('/forgotten-password/123/som3token/');

    var done = assert.async();

    onElement('.page-error.page-error-banned .message-body', function() {
      assert.ok(true, "Permission denied error page was displayed.");
      assert.equal(
        getElementText('.page .message-body .lead'),
        "This is test ban.",
        "Banned page displayed ban message.");
      done();
    });
  });

  QUnit.test('with backend rejection', function(assert) {
    var message = 'Some activation error.';
    $.mockjax({
      url: '/test-api/auth/change-password/123/som3token/',
      status: 400,
      responseText: {
        'detail': message
      }
    });

    app.router.route('/forgotten-password/123/som3token/');

    var done = assert.async();

    onElement('.message-body p', function() {
      assert.equal(getElementText('.message-body p:last-child'), message,
        "activation failed with backend message.");
      done();
    });
  });

  QUnit.test('form', function(assert) {
    $.mockjax({
      url: '/test-api/auth/change-password/123/som3token/',
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    app.router.route('/forgotten-password/123/som3token/');

    var done = assert.async();

    onElement('.well-form', function() {
      assert.ok(true, "change password for was displayed.");
      done();
    });
  });

  QUnit.test('empty form submission', function(assert) {
    $.mockjax({
      url: '/test-api/auth/change-password/123/som3token/',
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    app.router.route('/forgotten-password/123/som3token/');

    var done = assert.async();

    waitForElement('.well-form .btn-primary');
    click('.well-form .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Enter new password.",
        "form raised alert about empty input.");
      done();
    });
  });

  QUnit.test('invalid form submission', function(assert) {
    $.mockjax({
      url: '/test-api/auth/change-password/123/som3token/',
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    app.router.route('/forgotten-password/123/som3token/');

    var done = assert.async();

    waitForElement('.well-form input');

    fillIn('.well-form input', 'no');
    click('.well-form .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(
        getAlertMessage(),
        "Valid password must be at least 5 characters long.",
        "form raised alert about invalid new password.");
      done();
    });
  });

  QUnit.test('backend-rejected form submission', function(assert) {
    $.mockjax({
      url: '/test-api/auth/change-password/123/som3token/',
      type: 'get',
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    var message = "Backend error is raised!";
    $.mockjax({
      url: '/test-api/auth/change-password/123/som3token/',
      type: 'post',
      status: 400,
      responseText: {
        'detail': message
      }
    });

    app.router.route('/forgotten-password/123/som3token/');

    var done = assert.async();

    waitForElement('.well-form input');

    fillIn('.well-form input', 'pass123');
    click('.well-form .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), message,
        "form raised alert with error returned by backend.");
      done();
    });
  });

  QUnit.test('backend-accepted form submission', function(assert) {
    $.mockjax({
      url: '/test-api/auth/change-password/123/som3token/',
      type: 'get',
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    $.mockjax({
      url: '/test-api/auth/change-password/123/som3token/',
      type: 'post',
      status: 200,
      responseText: {
        'username': 'Bob'
      }
    });

    app.router.route('/forgotten-password/123/som3token/');

    var doneMessage = assert.async();
    var doneButton = assert.async();

    waitForElement('.well-form input');

    fillIn('.well-form input', 'pass123');
    click('.well-form .btn-primary');

    onElement('.message-body p.lead', function() {
      assert.equal(
        getElementText('.message-body p.lead'),
        "Bob, your password has been changed successfully.",
        "form displayed success message.");
      doneMessage();
    });

    onElement('.message-body .btn-default', function() {
      assert.ok(true, "form displayed sign-in button.");
      doneButton();
    });
  });
}());
