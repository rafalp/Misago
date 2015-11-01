(function () {
  'use strict';

  var app = null;

  QUnit.acceptance("Activate Account", {
    beforeEach: function() {
      app = initTestMisago();
    },
    afterEach: function() {
      app.destroy();
    }
  });

  QUnit.test('with backend banned', function(assert) {
    $.mockjax({
      url: '/test-api/auth/activate-account/123/som3token/',
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

    app.router.route('/activation/123/som3token/');

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
      url: '/test-api/auth/activate-account/123/som3token/',
      status: 400,
      responseText: {
        'detail': message
      }
    });

    app.router.route('/activation/123/som3token/');

    var done = assert.async();

    onElement('.message-body p', function() {
      assert.equal(getElementText('.message-body p:last-child'), message,
        "activation failed with backend message.");
      done();
    });
  });

  QUnit.test('with success', function(assert) {
    $.mockjax({
      url: '/test-api/auth/activate-account/123/som3token/',
      status: 200,
      responseText: {
        'username': 'Bob'
      }
    });

    app.router.route('/activation/123/som3token/');

    var done = assert.async();

    onElement('.message-body p.lead', function() {
      assert.equal(
        getElementText('.message-body p.lead'),
        "Bob, your account has been successfully activated!",
        "activation succeded.");
      done();
    });
  });
}());
