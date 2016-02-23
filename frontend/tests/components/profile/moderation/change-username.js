import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ChangeUsername from 'misago/components/profile/moderation/change-username'; // jshint ignore:line
import misago from 'misago/index';
import reducer from 'misago/reducers/profile';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
let profileMock = {
  id: 242,
  avatar_hash: 'original_hash',

  is_followed: false,
  followers: 0,

  api_url: {
    moderate_username: '/test-api/users/123/moderate-username/'
  }
};

describe("User Profile Moderation Change Username", function() {
  beforeEach(function() {
    misago._context = {
      SETTINGS: {
        username_length_min: 3,
        username_length_max: 8
      }
    };

    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    store.constructor();
    store.addReducer('profile', reducer, profileMock);

    store.addReducer('auth', function(state, action) {
      if (action || true) {
        return testUtils.mockUser();
      }
    }, {});
    store.addReducer('tick', function(state, action) {
      if (action || true) {
        return {'tick': 123};
      }
    }, {});
    store.addReducer('username-history', function(state, action) {
      if (action) {
        return action;
      } else {
        return {};
      }
    }, {});

    store.init();
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function(done) {
    $.mockjax({
      url: profileMock.api_url.moderate_username,
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeUsername profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount form', function(element) {
      assert.ok(element.length, "component loads");

      done();
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: profileMock.api_url.moderate_username,
      status: 500
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeUsername profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-message', function(element) {
      assert.equal(element.find('p.lead').text(), "Unknown error has occured.",
        "error message renders");

      done();
    });
  });

  it("handles load rejection", function(done) {
    $.mockjax({
      url: profileMock.api_url.moderate_username,
      status: 403,
      responseText: {
        detail: "You can't mod username!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeUsername profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-message', function(element) {
      assert.equal(element.find('p.lead').text(), "You can't mod username!",
        "error message renders");

      done();
    });
  });

  it("handles empty submission", function(done) {
    $.mockjax({
      url: profileMock.api_url.moderate_username,
      type: 'GET',
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeUsername profile={profileMock} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.equal(message.message, "This field is required.",
        "Rejection message is shown in snackbar.");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles invalid submission", function(done) {
    $.mockjax({
      url: profileMock.api_url.moderate_username,
      type: 'GET',
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeUsername profile={profileMock} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.equal(message.message,
        "Username can only contain latin alphabet letters and digits.",
        "Rejection message is shown in snackbar.");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#id_username', '###');
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles failed submission", function(done) {
    $.mockjax({
      url: profileMock.api_url.moderate_username,
      type: 'GET',
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    $.mockjax({
      url: profileMock.api_url.moderate_username,
      type: 'POST',
      status: 400,
      responseText: {
        detail: "Can't do it now!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeUsername profile={profileMock} />);
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.equal(message.message, "Can't do it now!",
        "Rejection message is shown in snackbar.");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#id_username', 'NewName');
      testUtils.simulateSubmit('#test-mount form');
    });
  });

  it("handles submission", function(done) {
    $.mockjax({
      url: profileMock.api_url.moderate_username,
      type: 'GET',
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    $.mockjax({
      url: profileMock.api_url.moderate_username,
      type: 'POST',
      status: 200,
      responseText: {
        username: 'NewName',
        slug: 'newname'
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeUsername profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount form', function() {
      testUtils.simulateChange('#id_username', 'NewName');
      testUtils.simulateSubmit('#test-mount form');

      window.setTimeout(function() {
        assert.equal(store.getState().profile.username, 'NewName',
          "profile username was updated");
        assert.equal(store.getState().profile.username, 'NewName',
          "profile slug was updated");

        assert.deepEqual(store.getState()['username-history'], {
          type: 'UPDATE_USERNAME',
          userId: 242,
          username: 'NewName',
          slug: 'newname'
        }, "name change was dispatched");

        done();
      }, 200);
    });
  });
});