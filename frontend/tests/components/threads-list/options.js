import assert from 'assert';
import moment from 'moment'; // jshint ignore:line
import React from 'react'; // jshint ignore:line
import ThreadOptions from 'misago/components/threads-list/thread/options'; // jshint ignore:line
import Store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

/* jshint ignore:start */
const thread = {
  id: 123,
  category: 3,
  title: "Doloremque alias repudiandae magnam facilis eligendi.",
  weight: 0,
  top_category: 3,
  replies: 2,
  has_unapproved_posts: false,
  started_on: moment("2016-04-17T16:37:42.317994Z"),
  last_post: 68707,
  last_poster_name: "Amya",
  last_poster_url: "/user/amya-1522/",
  last_post_on: moment("2016-04-17T16:37:42.364183Z"),
  is_read: true,
  is_unapproved: false,
  is_hidden: false,
  is_closed: false,
  absolute_url: "/threads/not-implemented-yet-123/",
  last_post_url: "/threads/not-implemented-yet-123/last/",
  new_post_url: "/threads/not-implemented-yet-123/new/",
  subscription: true,
  api_url: "/api/threads/123/",
  moderation: [true],
  acl: {
    can_edit: true,
    can_reply: true,
    can_hide: 2,
    can_close: 1,
    can_report: 1,
    can_see_reports: 1,
    can_move: 1,
    can_pin: 2,
    can_approve: 1
  }
};
/* jshint ignore:end */

describe("Threads List Thread Options", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ThreadOptions thread={thread} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .thread-options', function() {
      assert.ok(true, "component renders");

      done();
    });
  });

  it("hides selection when thread isnt moderable", function() {
    /* jshint ignore:start */
    const newThread = Object.assign({}, thread, {
      moderation: []
    })
    testUtils.render(<ThreadOptions thread={newThread} />);
    /* jshint ignore:end */

    assert.ok(!$('#test-mount .btn-checkbox').length,
      "thread without moderation options is not selectable");
  });

  it("selects thread", function(done) {
    Store._store = {
      dispatch: function(action) {
        assert.deepEqual(action, {
          type: 'SELECT_ITEM',
          item: 123
        });

        done();
      }
    };

    /* jshint ignore:start */
    testUtils.render(<ThreadOptions thread={thread} />);
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .btn-checkbox');
  });

  it("deselects thread", function(done) {
    Store._store = {
      dispatch: function(action) {
        assert.deepEqual(action, {
          type: 'SELECT_ITEM',
          item: 123
        });

        done();
      }
    };

    /* jshint ignore:start */
    testUtils.render(<ThreadOptions thread={thread} isSelected={true} />);
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .btn-checkbox');
  });
});
