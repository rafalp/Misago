import assert from 'assert';
import moment from 'moment'; // jshint ignore:line
import React from 'react'; // jshint ignore:line
import ListReady from 'misago/components/threads-list/list/ready'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

/* jshint ignore:start */
const props = {
  threads: [
    {
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
      moderation: [],
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
    },
    {
      id: 42,
      category: 4,
      title: "Sit facere pariatur consequatur qui voluptatum ducimus.",
      weight: 0,
      top_category: 3,
      replies: 3,
      has_unapproved_posts: false,
      started_on: moment("2016-04-17T16:37:13.224850Z"),
      last_post: 67637,
      last_poster_name: "Madora",
      last_poster_url: "/user/madora-1530/",
      last_post_on: moment("2016-04-17T16:37:13.287355Z"),
      is_read: true,
      is_unapproved: false,
      is_hidden: false,
      is_closed: false,
      absolute_url: "/threads/not-implemented-yet-42/",
      last_post_url: "/threads/not-implemented-yet-42/last/",
      new_post_url: "/threads/not-implemented-yet-42/new/",
      subscription: null,
      api_url: "/api/threads/42/",
      moderation: [],
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
    }
  ],

  categories: {
    2: {
      id: 2,
      parent: null,
      name: "Root",
      description: null,
      css_class: null,
      absolute_url: "/",
      api_url: {
        read: "/api/threads/read/"
      },
      special_role: true
    },
    3: {
      id: 3,
      parent: {
        id: 2,
        name: "Root",
        css_class: null,
        absolute_url: "/"
      },
      name: "First category",
      description: null,
      css_class: "accent",
      absolute_url: "/category/first-category-3/",
      api_url: {
        read: "/api/threads/read/?category=3"
      }
    },
    4: {
      id: 4,
      parent: {
        id: 3,
        name: "First category",
        css_class: null,
        absolute_url: "/category/first-category-3/"
      },
      name: "Herma Turnpike",
      description: null,
      css_class: null,
      absolute_url: "/category/herma-turnpike-4/",
      api_url: {
        read: "/api/threads/read/?category=4"
      }
    }
  },

  list: {
    type: 'all',
    path: '',
    name: gettext("All"),
    longName: gettext("All threads")
  },

  diffSize: 0,
  applyDiff: null,

  showOptions: false,
  selection: [],

  busyThreads: []
};
/* jshint ignore:end */

describe("Ready Threads List", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ListReady {...props} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .threads-list', function(element) {
      assert.ok(true, "component renders");

      assert.ok(!$(element).find('.thread-busy').length,
        "no thread is busy");
      assert.ok(!$(element).find('.thread-selected').length,
        "no thread is selected");

      assert.ok(!$(element).find('.thread-new').length,
        "no thread is unread");
      assert.ok(!$(element).find('.thread-new-posts').length,
        "no thread is unread");

      assert.ok(!$(element).find('.thread-pinned-globally').length,
        "no thread is pinned globally");
      assert.ok(!$(element).find('.thread-pinned-locally').length,
        "no thread is pinned locally");

      assert.ok(!$(element).find('.thread-unapproved').length,
        "no thread is unapproved");
      assert.ok(!$(element).find('.thread-unapproved-posts').length,
        "no thread has unapproved posts");

      assert.ok(!$(element).find('.thread-hidden').length,
        "no thread is hidden");

      assert.ok(!$(element).find('.thread-closed').length,
        "no thread is closed");

      assert.ok(!$(element).find('.thread-options').length,
        "no thread options are shown");

      done();
    });
  });

  it("renders with diff message", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    const applyDiff = function() {
      assert.ok(true, "apply diff message runs callback");

      done();
    };

    const newProps = Object.assign({}, props, {
      diffSize: 1,
      applyDiff
    });

    testUtils.render(<ListReady {...newProps} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .threads-list .btn', function(element) {
      assert.ok(true, "component renders");

      assert.equal($(element).find('.diff-message').text(),
        "There is 1 new or updated thread. Click this message to show it.",
        "message about new threads is displayed");

      testUtils.simulateClick('.btn');
    });
  });

  it("renders with state flags and options", function(done) {
    /* jshint ignore:start */
    let newProps = Object.assign({}, props, {
      showOptions: true,
      selection: [123],
      busyThreads: [42]
    });

    newProps.threads[0] = Object.assign({}, newProps.threads[0], {
      weight: 2,
      has_unapproved_posts: false,
      is_read: false,
      is_unapproved: true,
      is_hidden: true,
      is_closed: true,
      moderation: [true]
    });

    newProps.threads[1] = Object.assign({}, newProps.threads[1], {
      weight: 1,
      has_unapproved_posts: true,
      moderation: [true]
    });

    testUtils.render(<ListReady {...newProps} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .threads-list', function(element) {
      assert.ok(true, "component renders");

      assert.equal($(element).find('.thread-busy').length, 1,
        "one thread is busy");

      assert.equal($(element).find('.thread-selected').length, 1,
        "one thread is selected");

      assert.ok($(element).find('.thread-new').length,
        "unread threads are shown");
      assert.ok($(element).find('.thread-new-posts').length,
        "unread threads have state flag");

      assert.ok($(element).find('.thread-pinned-globally').length,
        "globally pinned thread has state flag");
      assert.ok($(element).find('.thread-pinned-locally').length,
        "locally pinned thread has state flag");

      assert.ok($(element).find('.thread-unapproved').length,
        "unapproved thread has state flag");
      assert.ok($(element).find('.thread-unapproved-posts').length,
        "thread with unapproved posts has state flag");

      assert.ok($(element).find('.thread-hidden').length,
        "hidden thread has state flag");

      assert.ok($(element).find('.thread-closed').length,
        "closed thread has state flag");

      assert.ok($(element).find('.thread-options').length,
        "thread options are shown");

      done();
    });
  });
});
