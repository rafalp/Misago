import assert from 'assert';
import moment from 'moment'; // jshint ignore:line
import React from 'react'; // jshint ignore:line
import UsernameHistory from 'misago/components/username-history/root'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Username History", function() {
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