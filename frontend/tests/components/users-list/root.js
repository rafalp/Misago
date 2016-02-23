import assert from 'assert';
import moment from 'moment'; // jshint ignore:line
import React from 'react'; // jshint ignore:line
import UsersList from 'misago/components/users-list/root'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

/* jshint ignore:start */
let users = [
  testUtils.mockUser({
    title: "Lorem ipsum",
    joined_on: moment(),
    status: {
      is_online: true,
    }
  })
];
/* jshint ignore:end */

describe("Users List", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders loaded", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <UsersList isLoaded={true} users={users} cols={4} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list .col-md-3', function() {
      assert.ok(true, "component renders with valid col class");
      assert.equal($('#test-mount .user-card').length, 1, "user card renders");
      assert.ok(!$('#test-mount .user-status').length, "status is hidden");

      done();
    });
  });

  it("renders loaded with different col class", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <UsersList isLoaded={true} users={users} cols={2} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list .col-md-6', function() {
      assert.ok(true, "component renders with valid col class");
      assert.equal($('#test-mount .user-card').length, 1, "user card renders");
      assert.ok(!$('#test-mount .user-status').length, "status is hidden");

      done();
    });
  });

  it("renders loaded with users status", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <UsersList isLoaded={true} users={users} cols={4} showStatus={true} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list .col-md-3', function() {
      assert.ok(true, "component renders with valid col class");
      assert.equal($('#test-mount .user-card').length, 1, "user card renders");
      assert.ok($('#test-mount .user-status').length, "status is shown");

      done();
    });
  });

  it("renders preview", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <UsersList isLoaded={false} cols={4} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list .col-md-3', function() {
      assert.ok(true, "component renders with valid col class");
      assert.equal($('#test-mount .user-card').length, 4, "user card renders");
      assert.ok(!$('#test-mount .user-status').length, "status is hidden");

      done();
    });
  });

  it("renders preview with different col class", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <UsersList isLoaded={false} cols={2} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list .col-md-6', function() {
      assert.ok(true, "component renders with valid col class");
      assert.equal($('#test-mount .user-card').length, 2, "user card renders");
      assert.ok(!$('#test-mount .user-status').length, "status is hidden");

      done();
    });
  });

  it("renders preview with users status", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <UsersList isLoaded={false} cols={4} showStatus={true} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list .col-md-3', function() {
      assert.ok(true, "component renders with valid col class");
      assert.equal($('#test-mount .user-card').length, 4, "user card renders");
      assert.ok($('#test-mount .user-status').length, "status is shown");

      done();
    });
  });
});
