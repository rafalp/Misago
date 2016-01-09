import assert from "assert";
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import { NoCaptcha, QACaptcha, ReCaptcha, Captcha } from 'misago/services/captcha';
import snackbar from 'misago/services/snackbar';

let captcha = null;
let snackbarStore = null;

describe("NoCaptcha", function() {
  it("always loads instantly", function(done) {
    captcha = new NoCaptcha();
    captcha.init({}, {}, {}, {});

    captcha.load().then(function() {
      assert.ok(true, "service loaded immediately");
      done();
    });
  });

  it("has no validator", function() {
    captcha = new NoCaptcha();
    assert.equal(captcha.validator(), null, "nocaptcha has no validator");
  });

  it("has no component", function() {
    captcha = new NoCaptcha();
    assert.equal(captcha.component(), null, "nocaptcha has no component");
  });
});

describe("QACaptcha", function() {
  beforeEach(function() {
    snackbarStore = window.snackbarStoreMock();
    snackbar.init(snackbarStore);
  });

  afterEach(function() {
    window.emptyTestContainers();
    window.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("handles successful load", function(done) {
    $.mockjax({
      url: '/test-api/captcha/',
      status: 200,
      responseText: {
        'question': "Test question",
        'help_text': "This is test quesiton for tests"
      }
    });

    captcha = new QACaptcha();
    captcha.init({
      get: function(setting) {
        assert.equal(setting, 'CAPTCHA_API_URL', "valid setting is used");
        return '/test-api/captcha/';
      }
    }, ajax, {}, {});

    captcha.load().then(function() {
      assert.equal(captcha.question, "Test question", "question was loaded");
      assert.equal(captcha.helpText, "This is test quesiton for tests",
        "question's help text was loaded");
      done();
    });
  });

  it("handles failed load", function(done) {
    $.mockjax({
      url: '/test-api/captcha/',
      status: 400,
      responseText: {
        'question': "Test question",
        'help_text': "This is test quesiton for tests"
      }
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Failed to load CAPTCHA.",
        type: 'error'
      }, "question failed to load from API");

      done();
    });

    captcha = new QACaptcha();
    captcha.init({
      get: function(setting) {
        assert.equal(setting, 'CAPTCHA_API_URL', "valid setting is used");
        return '/test-api/captcha/';
      }
    }, ajax, {}, snackbar);

    captcha.load().then(function() {
      assert.ok(false, "captcha should fail to load");
    }, function() {
      assert.ok(true, "captcha failed to load");
    });
  });

  it("is required", function() {
    captcha = new QACaptcha();
    assert.deepEqual(captcha.validator(), [], "qa-captcha is required");
  });

  it("renders component", function(done) {
    $.mockjax({
      url: '/test-api/captcha/',
      status: 200,
      responseText: {
        'question': "Test question",
        'help_text': "This is test quesiton for tests"
      }
    });

    captcha = new QACaptcha();
    captcha.init({
      get: function(setting) {
        assert.equal(setting, 'CAPTCHA_API_URL', "valid setting is used");
        return '/test-api/captcha/';
      }
    }, ajax, {}, {});

    captcha.load().then(function() {
      /* jshint ignore:start */
      ReactDOM.render(
        <div>
          {captcha.component({
            form: {
              state: {
                errors: {},

                isLoading: false,
                captcha: ''
              },

              bindInput: function(field) {
                assert.equal(field, 'captcha', "captcha is bound to state");
                return function() {
                  /* noop */
                };
              }
            }
          })}
        </div>,
        document.getElementById('test-mount')
      );
      /* jshint ignore:end */

      let element = $('#test-mount');
      assert.ok(element.length, "component renders");
      assert.equal(element.find('label').text().trim(), "Test question:",
        "label contains test question");
      assert.equal(element.find('p.help-block').text().trim(),
        "This is test quesiton for tests",
        "question's help text is displayed");
      done();
    });
  });
});

describe("ReCaptcha", function() {
  afterEach(function() {
    delete window.grecaptcha;

    window.emptyTestContainers();
    window.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("loads library", function(done) {
    captcha = new ReCaptcha();
    captcha.init({
      get: function(setting) {
        assert.equal(setting, 'SETTINGS', "settings object is accessed");
        return {
          recaptcha_site_key: 'aabbcc'
        };
      }
    }, {}, {
      include: function(url) {
        assert.ok(url, "library is requested from google servers");
      }
    }, {});

    captcha.load().then(function() {
      assert.ok('promise resolves');
      done();
    });

    window.setTimeout(function() {
      window.grecaptcha = {};
    }, 100);captcha = new ReCaptcha();
  });

  it("is required", function() {
    captcha = new ReCaptcha();
    assert.deepEqual(captcha.validator(), [], "recaptcha is required");
  });

  it("renders component", function(done) { // jshint ignore:line
    captcha = new ReCaptcha();
    captcha.init({
      get: function(setting) {
        assert.equal(setting, 'SETTINGS', "settings object is accessed");
        return {
          recaptcha_site_key: 'aabbcc'
        };
      }
    }, {}, {
      include: function(url) {
        assert.ok(url, "library is requested from google servers");
      }
    }, {});

    captcha.load().then(function() {
      /* jshint ignore:start */
      ReactDOM.render(
        <div>
          {captcha.component({
            form: {
              state: {
                errors: {},
                captcha: ''
              },

              bindInput: function() {
                return function(value) {
                  assert.deepEqual(value, {
                    target: {
                      value: 'valid-captcha'
                    }
                  }, "captcha is called");

                  done();
                };
              }
            }
          })}
        </div>,
        document.getElementById('test-mount')
      );
      /* jshint ignore:end */

      let element = $('#test-mount');
      assert.ok(element.length, "component renders");
      assert.equal(element.find('label').text().trim(), "Captcha:",
        "label is valid");
      assert.equal(element.find('p.help-block').text().trim(),
        "Please solve the quick test.",
        "field's help text is displayed");
    });

    window.setTimeout(function() {
      window.grecaptcha = {
        render: function(field, options) {
          assert.equal(field, 'recaptcha', "component is rendered in outlet");
          assert.equal(options.sitekey, 'aabbcc', "sitekey is passed to api");

          window.setTimeout(function() {
            options.callback('valid-captcha');
          }, 100);
        }
      };
    }, 100);
  });
});

describe("Captcha", function() {
  it("delegates load calls", function(done) {
    let captcha = new Captcha();
    captcha._captcha = {
      load: function() {
        assert.ok(true, "load call was delegated to strategy");
        done();
      }
    };

    captcha.load();
  });

  it("delegates validator calls", function(done) {
    let captcha = new Captcha();
    captcha._captcha = {
      validator: function() {
        assert.ok(true, "validator call was delegated to strategy");
        done();
      }
    };

    captcha.validator();
  });

  it("delegates component calls", function(done) {
    let captcha = new Captcha();
    captcha._captcha = {
      component: function() {
        assert.ok(true, "component call was delegated to strategy");
        done();
      }
    };

    captcha.component();
  });
});