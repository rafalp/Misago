import assert from 'assert';
import moment from 'moment';
import React from 'react'; // jshint ignore:line
import UserCard from 'misago/components/users-list/user-card'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Users List Item", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders with ui-preview", function(done) {
    let user = testUtils.mockUser({
      title: "Lorem ipsum",
      joined_on: moment()
    });

    /* jshint ignore:start */
    testUtils.render(
      <UserCard user={user} showStatus={true} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .user-card.ui-ready', function() {
      assert.ok(true, "component renders");
      assert.ok($('#test-mount .status-label.ui-preview').length,
        "status preview is rendered");

      assert.equal($('#test-mount .user-title').text().trim(), user.title,
        "user title is rendered");

      done();
    });
  });

  it("renders", function(done) {
    let user = testUtils.mockUser({
      title: "Lorem ipsum",
      status: {
        is_online: true
      },
      joined_on: moment()
    });

    /* jshint ignore:start */
    testUtils.render(
      <UserCard user={user} showStatus={true} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .user-card.ui-ready', function() {
      assert.ok(true, "component renders");

      assert.equal($('#test-mount .status-label').text().trim(), 'Online',
        "status label is rendered");

      assert.equal($('#test-mount .user-title').text().trim(), user.title,
        "user title is rendered");

      done();
    });
  });

  it("renders without status", function(done) {
    let user = testUtils.mockUser({
      title: "Lorem ipsum",
      status: {is_online: true},
      joined_on: moment()
    });

    /* jshint ignore:start */
    testUtils.render(
      <UserCard user={user} showStatus={false} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .user-card.ui-ready', function() {
      assert.ok(true, "component renders");

      assert.ok(!$('#test-mount .user-status').length, "status is hidden");

      assert.equal($('#test-mount .user-title').text().trim(), user.title,
        "user title is rendered");

      done();
    });
  });
});
