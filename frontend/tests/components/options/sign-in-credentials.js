import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Root from 'misago/components/options/sign-in-credentials/root'; // jshint ignore:line
import ChangeEmail from 'misago/components/options/sign-in-credentials/change-email'; // jshint ignore:line
import ChangePassword from 'misago/components/options/sign-in-credentials/change-password'; // jshint ignore:line
import misago from 'misago/index';
import snackbar from 'misago/services/snackbar';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
let user = testUtils.mockUser();

describe("Change E-mail Form", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ChangeEmail user={user} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount form', function() {
      assert.ok(true, "component renders");

      done();
    });
  });

  it("handles empty submit", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ChangeEmail user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Fill out all fields.",
        type: 'error'
      }, "error message was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: user.api_url.change_email,
      status: 400,
      responseText: {
        password: "Lol nope!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeEmail user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Lol nope!",
        type: 'error'
      }, "error message from backend was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_new_email', 'new@wt.com');
      testUtils.simulateChange('#test-mount form #id_password', 'p4ssw0rd');
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: user.api_url.change_email,
      status: 500
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeEmail user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Unknown error has occured.",
        type: 'error'
      }, "error message from backend was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_new_email', 'new@wt.com');
      testUtils.simulateChange('#test-mount form #id_password', 'p4ssw0rd');
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles successful submission", function(done) {
    $.mockjax({
      url: user.api_url.change_email,
      status: 200,
      responseText: {
        detail: "Well done gud!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeEmail user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Well done gud!",
        type: 'success'
      }, "success message from backend was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_new_email', 'new@wt.com');
      testUtils.simulateChange('#test-mount form #id_password', 'p4ssw0rd');
      testUtils.simulateSubmit('#test-mount form');
    });
  });
});

describe("Change Password Form", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);
    misago._context = {
      SETTINGS: {
        password_length_min: 4
      }
    };
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ChangePassword user={user} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount form', function() {
      assert.ok(true, "component renders");

      done();
    });
  });

  it("handles empty submit", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ChangePassword user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Fill out all fields.",
        type: 'error'
      }, "error message was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles passwords mismatch", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ChangePassword user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "New passwords are different.",
        type: 'error'
      }, "error message was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_new_password', 'newps');
      testUtils.simulateChange('#test-mount form #id_repeat_password', 'nesss');
      testUtils.simulateChange('#test-mount form #id_password', 'p4ssw0rd');
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: user.api_url.change_password,
      status: 400,
      responseText: {
        password: "Lol nope!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangePassword user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Lol nope!",
        type: 'error'
      }, "error message from backend was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_new_password', 'newps');
      testUtils.simulateChange('#test-mount form #id_repeat_password', 'newps');
      testUtils.simulateChange('#test-mount form #id_password', 'p4ssw0rd');
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: user.api_url.change_password,
      status: 500
    });

    /* jshint ignore:start */
    testUtils.render(<ChangePassword user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Unknown error has occured.",
        type: 'error'
      }, "error message from backend was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_new_password', 'newps');
      testUtils.simulateChange('#test-mount form #id_repeat_password', 'newps');
      testUtils.simulateChange('#test-mount form #id_password', 'p4ssw0rd');
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles successful submission", function(done) {
    $.mockjax({
      url: user.api_url.change_password,
      status: 200,
      responseText: {
        detail: "Well done gud!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangePassword user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Well done gud!",
        type: 'success'
      }, "success message from backend was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_new_password', 'newps');
      testUtils.simulateChange('#test-mount form #id_repeat_password', 'newps');
      testUtils.simulateChange('#test-mount form #id_password', 'p4ssw0rd');
      testUtils.simulateSubmit('#test-mount form');
    });
  });
});


describe("Change Sign In Credentials Root", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);
    misago._context = {
      FORGOTTEN_PASSWORD_URL: '/lolo/toto/',

      SETTINGS: {
        password_length_min: 4
      }
    };
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<Root user={user} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .message-line', function() {
      assert.equal($("#test-mount .message-line a").attr('href'),
        misago._context.FORGOTTEN_PASSWORD_URL,
        "change forgotten password url is rendered");

      done();
    });
  });
});