import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import misago from 'misago/index';
import { RegisterForm, RegisterComplete } from 'misago/components/register'; // jshint ignore:line
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';

let component = null;
let snackbarStore = null;

describe("Register Form", function() {
  beforeEach(function() {
    snackbarStore = window.snackbarStoreMock();
    snackbar.init(snackbarStore);
    window.initModal(modal);

    window.zxcvbn = function() {
      return {
        score: 2
      };
    };

    misago._context = {
      'SETTINGS': {
        captcha_type: 'no',

        username_length_min: 3,
        username_length_max: 10,

        password_length_min: 3
      },

      'USERS_API': '/test-api/users/',
      'TERMS_OF_SERVICE_URL': '/read-rules/'
    };

    /* jshint ignore:start */
    component = ReactDOM.render(
      <RegisterForm />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
  });

  afterEach(function() {
    delete window.zxcvbn;
    window.emptyTestContainers();
    window.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function() {
    let element = $('.modal-register');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('.modal-footer a').attr('href'), '/read-rules/',
      "registration has url to forum TOS");

    assert.equal(element.find('.modal-footer a').text().trim(),
      "By registering you agree to site's terms and conditions.",
      "registration has legal footnote");
  });

  it("handles empty submit", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Form contains errors.",
        type: "error"
      }, "rejests empty submission");
      done();
    });

    window.simulateSubmit('#test-mount form');
  });

  it("handles invalid submit", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Form contains errors.",
        type: "error"
      }, "rejests empty submission");
      done();
    });

    window.simulateChange('#id_username', 'lo');
    window.simulateChange('#id_email', 'nope');
    window.simulateChange('#id_password', 'sh');

    window.simulateSubmit('#test-mount form');
  });

  it("handles backend error", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Unknown error has occured.",
        type: 'error'
      }, "raised alert about backend error");
      done();
    });

    $.mockjax({
      url: '/test-api/users/',
      status: 500
    });

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_email', 'lorem@ipsum.com');
    window.simulateChange('#id_password', 'pass1234');

    window.simulateSubmit('#test-mount form');
  });

  it("handles rejected data", function(done) {
    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Form contains errors.",
        type: 'error'
      }, "raised alert about backend rejection");

      component.forceUpdate(function() {
        assert.deepEqual(component.state.errors.username,
          ['Dat username tou!'],
          "set backend username error to validation");
        assert.deepEqual(component.state.errors.password,
          ['Dat password tou!'],
          "set backend password error to validation");

        done();
      });
    });

    $.mockjax({
      url: '/test-api/users/',
      status: 400,
      responseText: {
        username: ['Dat username tou!'],
        password: ['Dat password tou!']
      }
    });

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_email', 'lorem@ipsum.com');
    window.simulateChange('#id_password', 'pass1234');

    window.simulateSubmit('#test-mount form');
  });

  it("from banned IP", function(done) {
    $.mockjax({
      url: '/test-api/users/',
      status: 403,
      responseText: {
        'ban': {
          'expires_on': null,
          'message': {
            'plain': 'Your ip is banned from registering.',
            'html': '<p>Your ip is banned from registering.</p>',
          }
        }
      }
    });

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_email', 'lorem@ipsum.com');
    window.simulateChange('#id_password', 'pass1234');

    window.simulateSubmit('#test-mount form');

    window.onElement('.page-error-banned .lead', function() {
      assert.equal(
        $('.page .message-body .lead p').text().trim(),
        "Your ip is banned from registering.",
        "displayed error banned page with ban message.");

      done();
    });
  });

  it("registered account", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    let callback = function(user) {
      assert.deepEqual(user, {
        'activation': 'user',
        'username': 'BobBoberson',
        'email': 'bob@boberson.com'
      }, "user data returned from backend is passed to success callback");
      done();
    };

    component = ReactDOM.render(
      <RegisterForm callback={callback}/>,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    $.mockjax({
      url: '/test-api/users/',
      status: 200,
      responseText: {
        'activation': 'user',
        'username': 'BobBoberson',
        'email': 'bob@boberson.com'
      }
    });

    window.simulateChange('#id_username', 'SomeFake');
    window.simulateChange('#id_email', 'lorem@ipsum.com');
    window.simulateChange('#id_password', 'pass1234');

    window.simulateSubmit('#test-mount form');
  });
});

describe("Register Complete", function() {
  afterEach(function() {
    window.emptyTestContainers();
  });

  it("renders user-activated message", function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <RegisterComplete activation="user"
                        username="Bob"
                        email="bob@boberson.com" />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount .modal-message');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('p').first().text().trim(),
      "Bob, your account has been created but you need to activate it before you will be able to sign in.",
      "component renders valid message");

    assert.equal(element.find('p').last().text().trim(),
      "We have sent an e-mail to bob@boberson.com with link that you have to click to activate your account.",
      "component renders valid activation instruction");
  });

  it("renders admin-activated message", function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <RegisterComplete activation="admin"
                        username="Bob"
                        email="bob@boberson.com" />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount .modal-message');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('p').first().text().trim(),
      "Bob, your account has been created but board administrator will have to activate it before you will be able to sign in.",
      "component renders valid message");

    assert.equal(element.find('p').last().text().trim(),
      "We will send an e-mail to bob@boberson.com when this takes place.",
      "component renders valid activation instruction");
  });
});