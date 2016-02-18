import assert from 'assert';
import React from 'react'; // jshint ignore:line
import AvatarControls from 'misago/components/profile/moderation/avatar-controls'; // jshint ignore:line
import snackbar from 'misago/services/snackbar';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
let profileMock = {
  is_followed: false,
  followers: 0,

  api_url: {
    moderate_avatar: '/test-api/users/123/moderate_avatar/'
  }
};

describe("User Profile Moderation Avatar Controls", function() {
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
    $.mockjax({
      url: profileMock.api_url.moderate_avatar,
      status: 200,
      responseText: {
        is_avatar_locked: false,
        avatar_lock_user_message: null,
        avatar_lock_staff_message: null
      }
    });

    /* jshint ignore:start */
    testUtils.render(<AvatarControls profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount form', function(element) {
      assert.ok(element.length, "component loads");

      done();
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: profileMock.api_url.moderate_avatar,
      status: 500
    });

    /* jshint ignore:start */
    testUtils.render(<AvatarControls profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-message', function(element) {
      assert.equal(element.find('p.lead').text(), "Unknown error has occured.",
        "error message renders");

      done();
    });
  });

  it("handles load rejection", function(done) {
    $.mockjax({
      url: profileMock.api_url.moderate_avatar,
      status: 403,
      responseText: {
        detail: "You can't mod user avatar!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<AvatarControls profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-message', function(element) {
      assert.equal(element.find('p.lead').text(), "You can't mod user avatar!",
        "error message renders");

      done();
    });
  });
});