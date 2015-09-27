(function () {
  'use strict';

  var app = null;

  QUnit.acceptance("Legal Pages", {
    beforeEach: function() {
      app = initTestMisago();
    },
    afterEach: function() {
      app.destroy();
    }
  });

  QUnit.test('privacy policy link', function(assert) {
    var doneHidden = assert.async();
    var doneVisible = assert.async();

    app.settings.terms_of_service = false;
    app.settings.privacy_policy = false;

    m.redraw();

    onElement('.forum-footer', function() {
      assert.equal(
        getElementText('.footer-nav'), "",
        "Privacy policy link is hidden in footer.");
      doneHidden();

      app.settings.privacy_policy = true;

      m.redraw();

      onElement('.footer-nav a', function() {
        assert.equal(
          getElementText('.footer-nav a'), "Test Privacy Policy",
          "Privacy policy link is displayed in footer.");
        doneVisible();
      });
    });
  });

  QUnit.test('terms of service link', function(assert) {
    var doneHidden = assert.async();
    var doneVisible = assert.async();

    app.settings.privacy_policy = false;
    app.settings.terms_of_service = false;

    m.redraw();

    onElement('.forum-footer', function() {
      assert.equal(
        getElementText('.footer-nav'), "",
        "Terms link is hidden in footer.");
      doneHidden();

      app.settings.terms_of_service = true;

      m.redraw();

      onElement('.footer-nav a', function() {
        assert.equal(
          getElementText('.footer-nav a'), "Test Terms",
          "Terms link is displayed in footer.");
        doneVisible();
      });
    });
  });

  QUnit.test('legals pages disabled', function(assert) {
    app.settings.privacy_policy = null;
    app.settings.terms_of_service = null;

    $.mockjax({
      url: '/test-api/legal-pages/privacy-policy/',
      status: 404,
      responseText: {'detail': 'Not found'}
    });
    $.mockjax({
      url: '/test-api/legal-pages/terms-of-service/',
      status: 404,
      responseText: {'detail': 'Not found'}
    });

    var donePrivacyPolicy = assert.async();
    var doneTermsOfService = assert.async();

    assert.ok(!getElement('.footer-nav a').length,
      "footer nav has no legal pages links");

    m.route('/privacy-policy/');
    onElement('.error-page.error-404-page', function() {
      assert.ok(true, "Unset privacy policy returned 404 page.");
      donePrivacyPolicy();
    });

    m.route('/terms-of-service/');
    onElement('.error-page.error-404-page', function() {
      assert.ok(true, "Unset terms of service returned 404 page.");
      doneTermsOfService();
    });
  });

  QUnit.test('privacy policy page', function(assert) {
    $.mockjax({
      url: '/test-api/legal-pages/privacy-policy/',
      status: 200,
      responseText: {
        'id': 'privacy-policy',
        'link': '',
        'title': 'Backend Policy',
        'body': '<p>Lorem ipsum dolor met sit amet elit.</p>'
      }
    });

    var done = assert.async();

    m.route('/privacy-policy/');
    onElement('.legal-page', function() {
      assert.equal(
        getElementText('.page-header h1'), 'Backend Policy',
        "Privacy Policy page has been rendered.");
      assert.equal(
        getElementText('.container p'), 'Lorem ipsum dolor met sit amet elit.',
        "Privacy Policy body has been rendered.");
      done();
    });
  });

  QUnit.test('terms of service page', function(assert) {
    $.mockjax({
      url: '/test-api/legal-pages/terms-of-service/',
      status: 200,
      responseText: {
        'id': 'terms-of-service',
        'link': '',
        'title': 'Backend Terms',
        'body': '<p>Lorem ipsum dolor met sit amet elit.</p>'
      }
    });

    var done = assert.async();

    m.route('/terms-of-service/');
    onElement('.legal-page', function() {
      assert.equal(
        getElementText('.page-header h1'), 'Backend Terms',
        "Terms of Service page has been rendered.");
      assert.equal(
        getElementText('.container p'), 'Lorem ipsum dolor met sit amet elit.',
        "Terms of Service body has been rendered.");
      done();
    });
  });
}());
