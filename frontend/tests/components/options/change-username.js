import assert from 'assert';
import moment from 'moment'; // jshint ignore:line
import React from 'react'; // jshint ignore:line
import Root, { ChangeUsername, NoChangesLeft, ChangeUsernameLoading, UsernameHistory } from 'misago/components/options/change-username'; // jshint ignore:line
import misago from 'misago/index';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
let user = testUtils.mockUser();
user.acl.name_changes_expire = 2;

describe("Change Username Form", function() {
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
    let options = {
      changes_left: 5,
      length_min: 3,
      length_max: 14,
      next_on: null
    };

    testUtils.render(
      <ChangeUsername user={user}
                      options={options} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .form-horizontal', function() {
      assert.ok(true, "component renders");

      assert.equal($('#test-mount form .help-block').text().trim(),
        "You can change your username 5 more times. Used changes redeem after 2 days.",
        "valid help text is displayed in form");
      done();
    });
  });

  it("handles empty submit", function(done) {
    /* jshint ignore:start */
    let options = {
      changes_left: 5,
      length_min: 3,
      length_max: 14,
      next_on: null
    };

    testUtils.render(
      <ChangeUsername user={user}
                      options={options} />
    );
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "This field is required.",
        type: 'error'
      }, "error message was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles invalid submit", function(done) {
    /* jshint ignore:start */
    let options = {
      changes_left: 5,
      length_min: 10,
      length_max: 14,
      next_on: null
    };

    testUtils.render(
      <ChangeUsername user={user}
                      options={options} />
    );
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Username must be at least 10 characters long.",
        type: 'error'
      }, "error message was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_username', 'NewName');
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: user.api_url.username,
      status: 400,
      responseText: {
        detail: "Lol nope!"
      }
    });

    /* jshint ignore:start */
    let options = {
      changes_left: 5,
      length_min: 3,
      length_max: 14,
      next_on: null
    };

    testUtils.render(
      <ChangeUsername user={user}
                      options={options} />
    );
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Lol nope!",
        type: 'error'
      }, "error message from backend was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_username', 'Newt');
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: user.api_url.username,
      status: 500
    });

    /* jshint ignore:start */
    let options = {
      changes_left: 5,
      length_min: 3,
      length_max: 14,
      next_on: null
    };

    testUtils.render(
      <ChangeUsername user={user}
                      options={options} />
    );
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Unknown error has occured.",
        type: 'error'
      }, "error message from backend was shown");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_username', 'Newt');
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles successfull submission", function(done) { // jshint ignore:line
    $.mockjax({
      url: user.api_url.username,
      status: 200,
      responseText: {
        username: 'Newt',
        slug: 'newt',
        options: {
          changes_left: 4,
          length_min: 3,
          length_max: 14,
          next_on: null
        }
      }
    });

    /* jshint ignore:start */
    let options = {
      changes_left: 5,
      length_min: 3,
      length_max: 14,
      next_on: null
    };

    let callback = function(username, slug, options) {
      assert.equal(username, 'Newt', "new username is passed to callback");
      assert.equal(slug, 'newt', "new slug is passed to callback");
      assert.deepEqual(options, {
          changes_left: 4,
          length_min: 3,
          length_max: 14,
          next_on: null
      }, "new options are passed to callback");

      done();
    };

    testUtils.render(
      <ChangeUsername user={user}
                      options={options}
                      complete={callback} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#test-mount form #id_username', 'newt');
      testUtils.simulateSubmit('#test-mount form');
    });
  });
});

describe("No Changes Left Message", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    let options = {
      changes_left: 5,
      length_min: 3,
      length_max: 14,
      next_on: null
    };

    testUtils.render(<NoChangesLeft options={options} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .panel-message-body', function() {
      assert.ok(true, "component renders");

      assert.equal($('#test-mount .help-block').text().trim(),
        "You have used up available name changes.",
        "valid help text is displayed in message");
      done();
    });
  });

  it("renders with next change message", function(done) {
    /* jshint ignore:start */
    let options = {
      changes_left: 5,
      length_min: 3,
      length_max: 14,
      next_on: moment().add(5, 'days')
    };

    testUtils.render(<NoChangesLeft options={options} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .panel-message-body', function() {
      assert.ok(true, "component renders");
      assert.equal($('#test-mount .help-block').text().trim(),
        "You will be able to change your username in 5 days.",
        "valid help text is displayed in message");
      done();
    });
  });
});

describe("Change Username Loading", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ChangeUsernameLoading />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .panel-body-loading', function() {
      assert.ok(true, "component renders");

      done();
    });
  });
});

describe("Username History Changes List", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders preview", function(done) {
    /* jshint ignore:start */
    testUtils.render(<UsernameHistory isLoaded={false} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .username-history.ui-preview', function() {
      assert.ok(true, "component renders");

      done();
    });
  });

  it("renders empty", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <UsernameHistory isLoaded={true}
                       changes={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .empty-message', function() {
      assert.equal($('.empty-message').text().trim(),
        "No name changes have been recorded for your account.",
        "component renders with message");

      done();
    });
  });

  it("renders with two changes", function(done) {
    /* jshint ignore:start */
    let changes = [
      {
        id: 27,
        changed_by: {
          id: 1,
          username: "rafalp",
          slug: "rafalp",
          avatar_hash: "5c6a04b4",
          absolute_url: "/user/rafalp-1/"
        },
        changed_by_username: "rafalp",
        changed_on: moment(),
        new_username: "Newt",
        old_username: "LoremIpsum"
      },
      {
        id: 26,
        changed_by: {
          id: 1,
          username: "rafalp",
          slug: "rafalp",
          avatar_hash: "5c6a04b4",
          absolute_url: "/user/rafalp-1/"
        },
        changed_by_username: "rafalp",
        changed_on: moment(),
        new_username: "LoremIpsum",
        old_username: "BobBoberson"
      }
    ];

    testUtils.render(
      <UsernameHistory isLoaded={true}
                       changes={changes} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .username-history.ui-ready', function() {
      assert.equal($('#test-mount .list-group-item').length, 2,
        "component renders with two items");

      done();
    });
  });
});

describe("Change Username Integration", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);
    testUtils.initEmptyStore(store);

    misago._context = {
      USERNAME_CHANGES_API: '/test-api/name-history/'
    };
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function(done) {
    $.mockjax({
      url: user.api_url.username,
      status: 200,
      responseText: {
        changes_left: 2,
        length_min: 3,
        length_max: 14,
        next_on: null
      }
    });

    $.mockjax({
      url: '/test-api/name-history/?user=' + user.id,
      status: 200,
      responseText: {
        results: []
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Root user={user}
            username-history={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .username-history.ui-ready', function() {
      assert.ok(true, "root component renders");
      done();
    });
  });

  it("renders with no changes left", function(done) {
    $.mockjax({
      url: user.api_url.username,
      status: 200,
      responseText: {
        changes_left: 0,
        length_min: 3,
        length_max: 14,
        next_on: null
      }
    });

    $.mockjax({
      url: '/test-api/name-history/?user=' + user.id,
      status: 200,
      responseText: {
        results: []
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Root user={user}
            username-history={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .panel-message-body', function() {
      assert.ok(true, "root component renders");

      assert.equal($('#test-mount .help-block').text().trim(),
        "You have used up available name changes.",
        "valid help text is displayed in message");
      done();
    });
  });

  it("handles username change", function(done) {
    $.mockjax({
      url: user.api_url.username,
      status: 200,
      type: 'GET',
      responseText: {
        changes_left: 2,
        length_min: 3,
        length_max: 14,
        next_on: null
      }
    });

    $.mockjax({
      url: user.api_url.username,
      status: 200,
      type: 'POST',
      responseText: {
        username: 'Newt',
        slug: 'newt',
        options: {
          changes_left: 2,
          length_min: 3,
          length_max: 14,
          next_on: null
        }
      }
    });

    $.mockjax({
      url: '/test-api/name-history/?user=' + user.id,
      status: 200,
      responseText: {
        results: []
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Root user={user}
            username-history={[]} />
    );
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Your username has been changed successfully.",
        type: 'success'
      }, "error message was shown");

      done();
    });

    testUtils.onElement('#test-mount form #id_username', function() {
      testUtils.simulateChange('#test-mount form #id_username', 'newt');
      testUtils.simulateSubmit('#test-mount form');
    });
  });
});