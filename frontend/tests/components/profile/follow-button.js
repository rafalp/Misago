import assert from 'assert';
import React from 'react'; // jshint ignore:line
import FollowButton from 'misago/components/profile/follow-button'; // jshint ignore:line
import reducer, { patch } from 'misago/reducers/profile';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
let profileMock = {
  is_followed: false,
  followers: 0,

  api_url: {
    follow: '/test-api/users/123/follow/'
  }
};

describe("Follow Button", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    store.constructor();
    store.addReducer('profile', reducer, profileMock);

    store.addReducer('auth', function(state, action) {
      if (action || true) {
        return {};
      }
    }, {});
    store.addReducer('tick', function(state, action) {
      if (action || true) {
        return {'tick': 123};
      }
    }, {});

    store.init();
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders unfollowed", function() {
    /* jshint ignore:start */
    testUtils.render(<FollowButton profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .btn-follow');
    assert.ok(element.length, "component renders");
    assert.equal(element.find('.material-icon').text(), 'favorite_border',
      "button has valid icon");
    assert.ok(element.text().indexOf("Follow") > 0,
      "button has valid label");
  });

  it("renders followed", function() {
    /* jshint ignore:start */
    let followedProfile = Object.assign({}, profileMock, {is_followed: true});
    testUtils.render(<FollowButton profile={followedProfile} />);
    /* jshint ignore:end */

    let element = $('#test-mount .btn-following');
    assert.ok(element.length, "component renders");
    assert.equal(element.find('.material-icon').text(), 'favorite',
      "button has valid icon");
    assert.ok(element.text().indexOf("Following") > 0,
      "button has valid label");
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: profileMock.api_url.follow,
      status: 500
    });

    /* jshint ignore:start */
    testUtils.render(<FollowButton profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .btn-follow');

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Unknown error has occured.",
        type: 'error'
      }, "error message was shown");

      done();
    });
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: profileMock.api_url.follow,
      status: 400,
      responseText: {
        detail: "You can't follow yourself!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<FollowButton profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .btn-follow');

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "You can't follow yourself!",
        type: 'error'
      }, "error message was shown");

      done();
    });
  });

  it("handles follow", function(done) {
    $.mockjax({
      url: profileMock.api_url.follow,
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    /* jshint ignore:start */
    testUtils.render(<FollowButton profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .btn-follow');

    window.setTimeout(function() {
      let state = store.getState().profile;

      assert.ok(state.is_followed, "followed flag was set");
      assert.equal(state.followers, 1, "followers count was increased");
      assert.equal(state.detail, 'ok', "profile was synced with backend state");

      done();
    }, 200);
  });

  it("handles unfollow", function(done) {
    $.mockjax({
      url: profileMock.api_url.follow,
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    store.dispatch(patch({
      is_followed: true,
      followers: 1
    }));

    /* jshint ignore:start */
    let followedProfile = Object.assign({}, profileMock, {
      is_followed: true,
      followers: 1
    });
    testUtils.render(<FollowButton profile={followedProfile} />);
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .btn-following');

    window.setTimeout(function() {
      let state = store.getState().profile;

      assert.ok(!state.is_followed, "followed flag was unset");
      assert.equal(state.followers, 0, "followers count was decreased");
      assert.equal(state.detail, 'ok', "profile was synced with backend state");

      done();
    }, 200);
  });
});