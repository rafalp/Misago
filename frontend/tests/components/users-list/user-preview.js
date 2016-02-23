import assert from 'assert';
import React from 'react'; // jshint ignore:line
import UserPreview from 'misago/components/users-list/user-preview'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Users List Item Preview", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <UserPreview showStatus={true} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .user-card.ui-preview', function() {
      assert.ok(true, "component renders");

      assert.ok($('#test-mount .user-status').length, "status is rendered");

      done();
    });
  });

  it("renders without status", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <UserPreview showStatus={false} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .user-card.ui-preview', function() {
      assert.ok(true, "component renders");

      assert.ok(!$('#test-mount .user-status').length, "status is hidden");

      done();
    });
  });
});
