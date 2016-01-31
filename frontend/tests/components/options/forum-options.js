import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ForumOptions from 'misago/components/options/forum-options'; // jshint ignore:line
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
let user = testUtils.mockUser();

describe("Forum Options Form", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);
    testUtils.initEmptyStore(store);
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ForumOptions user={user} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .form-horizontal', function() {
      assert.ok(true, "component renders");
      done();
    });
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: user.api_url.options,
      status: 400,
      responseText: {
        detail: "Lol nope!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ForumOptions user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Please reload page and try again.",
        type: 'error'
      }, "error message was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: user.api_url.options,
      status: 500
    });

    /* jshint ignore:start */
    testUtils.render(<ForumOptions user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Unknown error has occured.",
        type: 'error'
      }, "error message was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("submits successfully", function(done) {
    $.mockjax({
      url: user.api_url.options,
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ForumOptions user={user} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Your forum options have been changed.",
        type: 'success'
      }, "success message was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateSubmit('#test-mount form');
    });
  });
});