import assert from 'assert';
import moment from 'moment';
import React from 'react'; // jshint ignore:line
import Root, { RankUsers, RankUsersPager, RankUserCard, RankUsersLoading } from 'misago/components/users/rank'; // jshint ignore:line
import misago from 'misago/index';
import reducer from 'misago/reducers/users';
import ajax from 'misago/services/ajax';
import polls from 'misago/services/polls';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;

describe("Rank Users List", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders users", function(done) {
    /* jshint ignore:start */
    let users = [
      testUtils.mockUser({
        id: 123,
        title: "Lorem ipsum",
        status: {is_online: true},
        joined_on: moment()
      }),
      testUtils.mockUser({
        id: 122,
        status: {is_online: true},
        joined_on: moment()
      })
    ];

    let state = {
      count: 2,
      page: 1,
      pages: 2,
      page_range: [1, 2],
      first: 1,
      previous: null,
      next: 2,
      last: 2,
      before: 0,
      more: 1
    };

    testUtils.render(
      <RankUsers baseUrl='/users/'
                 users={users}
                 {...state} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list.ui-ready', function() {
      assert.ok(true, "component renders");

      assert.ok($('#test-mount .pager-undercontent').length,
        "paginator is rendered");

      assert.equal($('#test-mount .user-card').length, 2,
        "two users are rendered");

      done();
    });
  });
});

describe("Rank User Card", function() {
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
      <RankUserCard user={user} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .user-card', function() {
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
      status: {is_online: true},
      joined_on: moment()
    });

    /* jshint ignore:start */
    testUtils.render(
      <RankUserCard user={user} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .user-card', function() {
      assert.ok(true, "component renders");

      assert.equal($('#test-mount .status-label').text().trim(), 'Online',
        "status label is rendered");

      assert.equal($('#test-mount .user-title').text().trim(), user.title,
        "user title is rendered");

      done();
    });
  });
});

describe("Rank Users Pager", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    let state = {
      baseUrl: '/users/rank-slug/',

      count: 10,
      page: 2,
      pages: 3,
      page_range: [1, 2, 3],
      first: 1,
      previous: null,
      next: 3,
      last: 3,
      before: 10,
      more: 10
    };

    testUtils.render(
      <RankUsersPager {...state} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .pager-undercontent', function() {
      assert.ok(true, "component renders");

      assert.ok($('#test-mount .pager .previous').length, "prev page renders");
      assert.ok($('#test-mount .pager .next').length, "next page renders");
      assert.equal($('#test-mount .pager-progress-bar li').length, 3,
        "progress bar renders");

      assert.equal($('#test-mount .pager-progress-bar .active').text().trim(),
        '2',
        "valid page is active in progress bar");

      done();
    });
  });

  it("renders without next page", function(done) {
    /* jshint ignore:start */
    let state = {
      baseUrl: '/users/rank-slug/',

      count: 10,
      page: 3,
      pages: 3,
      page_range: [1, 2, 3],
      first: 1,
      previous: null,
      next: null,
      last: null,
      before: 10,
      more: 0
    };

    testUtils.render(
      <RankUsersPager {...state} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .pager-undercontent', function() {
      assert.ok(true, "component renders");

      assert.ok($('#test-mount .pager .previous').length, "prev page renders");
      assert.ok(!$('#test-mount .pager .next').length, "next not rendering");
      assert.equal($('#test-mount .pager-progress-bar li').length, 3,
        "progress bar renders");

      assert.equal($('#test-mount .pager-progress-bar .active').text().trim(),
        '3',
        "valid page is active in progress bar");

      done();
    });
  });

  it("renders without prev page", function(done) {
    /* jshint ignore:start */
    let state = {
      baseUrl: '/users/rank-slug/',

      count: 10,
      page: 1,
      pages: 3,
      page_range: [1, 2, 3],
      first: null,
      previous: null,
      next: 2,
      last: 3,
      before: 0,
      more: 10
    };

    testUtils.render(
      <RankUsersPager {...state} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .pager-undercontent', function() {
      assert.ok(true, "component renders");

      assert.ok(!$('#test-mount .pager .previous').length,
        "prev page is not rendering");
      assert.ok($('#test-mount .pager .next').length, "next page renders");
      assert.equal($('#test-mount .pager-progress-bar li').length, 3,
        "progress bar renders");

      assert.equal($('#test-mount .pager-progress-bar .active').text().trim(),
        '1',
        "valid page is active in progress bar");

      done();
    });
  });
});

describe("Rank Users Loading", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<RankUsersLoading />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list.ui-preview', function() {
      assert.ok(true, "component renders");

      done();
    });
  });
});
describe("Rank Users Root", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    polls.init(ajax, snackbar);

    testUtils.contextGuest(misago);

    misago._context = Object.assign(misago._context, {
      USERS_LIST_URL: '/users/',
      USERS_API: '/test-api/users/',

      USERS_LISTS: [
        {
          component: "rank",
          name: "Forum team",
          slug: 'forum-team',
          css_class: 'forum-team',
          description: {
            plain: "This is forum team rank.",
            html: "<p class=\"test-description\">This is forum team rank.</p>"
          }
        }
      ]
    });

    store.constructor();
    store.addReducer('users', reducer, []);
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

  it("renders preloaded", function(done) {
    let data = {
      results: [
        testUtils.mockUser({
          id: 123,
          title: "Lorem ipsum",
          status: {is_online: true}
        }),
        testUtils.mockUser({
          id: 122,
          status: {is_online: true}
        })
      ],

      count: 10,
      page: 1,
      pages: 1,
      page_range: [1],
      first: null,
      previous: null,
      next: null,
      last: null,
      before: 0,
      more: 0
    };

    $.mockjax({
      url: '/test-api/users/?list=rank&rank=forum-team&page=1',
      status: 200,
      responseText: data
    });

    misago._context.USERS = data;

    /* jshint ignore:start */
    let rank = {
      name: "Forum team",
      slug: 'forum-team',
      css_class: 'forum-team',
      description: {
        plain: "This is forum team rank.",
        html: "<p class=\"test-description\">This is forum team rank.</p>"
      }
    };

    testUtils.render(
      <Root user={misago._context.user}
            users={[]}
            tick={123}
            route={{rank: rank}}
            params={{}} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list.ui-ready', function() {
      assert.ok(true, "component renders");

      assert.equal($('#test-mount p.test-description').text().trim(),
        "This is forum team rank.",
        "rank description was displayed");

      done();
    });
  });

  it("loads", function(done) {
    let data = {
      results: [
        testUtils.mockUser({
          id: 123,
          title: "Lorem ipsum",
          status: {is_online: true}
        }),
        testUtils.mockUser({
          id: 122,
          status: {is_online: true}
        })
      ],

      count: 10,
      page: 1,
      pages: 1,
      page_range: [1],
      first: null,
      previous: null,
      next: null,
      last: null,
      before: 0,
      more: 0
    };

    $.mockjax({
      url: '/test-api/users/?list=rank&rank=forum-team&page=1',
      status: 200,
      responseText: data
    });

    /* jshint ignore:start */
    let rank = {
      name: "Forum team",
      slug: 'forum-team',
      css_class: 'forum-team',
      description: {
        plain: "This is forum team rank.",
        html: "<p class=\"test-description\">This is forum team rank.</p>"
      }
    };

    testUtils.render(
      <Root user={misago._context.user}
            users={[]}
            tick={123}
            route={{rank: rank}}
            params={{}} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list.ui-ready', function() {
      assert.ok(true, "component renders");

      assert.equal($('#test-mount p.test-description').text().trim(),
        "This is forum team rank.",
        "rank description was displayed");

      done();
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: '/test-api/users/?list=rank&rank=forum-team&page=1',
      status: 500
    });

    /* jshint ignore:start */
    let rank = {
      name: "Forum team",
      slug: 'forum-team',
      css_class: 'forum-team',
      description: {
        plain: "This is forum team rank.",
        html: "<p class=\"test-description\">This is forum team rank.</p>"
      }
    };

    testUtils.render(
      <Root user={misago._context.user}
            users={[]}
            tick={123}
            route={{rank: rank}}
            params={{}} />
    );
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Unknown error has occured.",
        type: 'error'
      }, "error message was shown");

      done();
    });
  });
});