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
      assert.ok($('#test-mount .status-label.ui-preview-text').length,
        "status preview is rendered");

      assert.equal($('#test-mount .user-title').text(), user.title,
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

      assert.equal($('#test-mount .status-label').text(), 'Online',
        "status label is rendered");

      assert.equal($('#test-mount .user-title').text(), user.title,
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

      assert.equal($('#test-mount .user-title').text(), user.title,
        "user title is rendered");

      done();
    });
  });

  it("renders with rank", function(done) {
    let user = testUtils.mockUser({
      title: "Lorem ipsum",
      status: {is_online: true},
      joined_on: moment(),
      rank: {
        name: 'Some Yolo',
        is_tab: false,
        absolute_url: '/users/ranks/some-yolo/'
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <UserCard user={user} showRank={true} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .user-card.ui-ready', function() {
      assert.ok(true, "component renders");

      assert.ok(!$('#test-mount .user-status').length, "status is hidden");

      assert.equal($('#test-mount .user-title').text(), user.title,
        "user title is rendered");

      assert.equal($('#test-mount .rank-name').text(), user.rank.name,
        "user rank is rendered");

      done();
    });
  });

  it("renders with rank url", function(done) {
    let user = testUtils.mockUser({
      title: "Lorem ipsum",
      status: {is_online: true},
      joined_on: moment(),
      rank: {
        name: 'Some Yolo',
        is_tab: true,
        absolute_url: '/users/ranks/some-yolo/'
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <UserCard user={user} showRank={true} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .user-card.ui-ready', function() {
      assert.ok(true, "component renders");

      assert.ok(!$('#test-mount .user-status').length, "status is hidden");

      assert.equal($('#test-mount .user-title').text(), user.title,
        "user title is rendered");

      assert.equal($('#test-mount .rank-name').text(), user.rank.name,
        "user rank is rendered");

      assert.equal($('#test-mount .rank-name').attr('href'),
        user.rank.absolute_url,
        "user rank is url to rank users list");

      done();
    });
  });
});
