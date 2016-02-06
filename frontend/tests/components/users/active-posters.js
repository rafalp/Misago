import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Root, { ActivePosters, ActivePoster, ActivePostersLoading, NoActivePosters } from 'misago/components/users/active-posters'; // jshint ignore:line
import misago from 'misago/index';
import reducer from 'misago/reducers/users';
import ajax from 'misago/services/ajax';
import polls from 'misago/services/polls';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;

describe("Active Posters List", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders users", function(done) {
    /* jshint ignore:start */
    let users = [
      testUtils.mockUser({
        id: 123,
        meta: {score: 42},
        title: "Lorem ipsum",
        status: {is_online: true}
      }),
      testUtils.mockUser({
        id: 122,
        meta: {score: 36},
        status: {is_online: true}
      })
    ];

    testUtils.render(
      <ActivePosters users={users}
                     trackedPeriod={30}
                     count={2} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .active-posters.ui-ready', function() {
      assert.ok(true, "component renders");

      assert.equal($('#test-mount p.lead').text().trim(),
        "2 most active posters from last 30 days.",
        "lead message was displayed");

      assert.equal($('#test-mount .list-group-item').length, 2,
        "two users are rendered");

      done();
    });
  });
});

describe("Active Poster", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders with ui-preview", function(done) {
    let user = testUtils.mockUser();
    user.meta = {score: 42};
    user.title = "Lorem ipsum";

    /* jshint ignore:start */
    testUtils.render(
      <ActivePoster user={user} rank={user.rank} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .list-group-item', function() {
      assert.ok(true, "component renders");
      assert.ok($('#test-mount .status-icon.ui-preview').length,
        "status preview is rendered");

      assert.equal($('#test-mount .rank-name').text().trim(), user.rank.name,
        "rank name is rendered");

      assert.equal($('#test-mount .user-title').text().trim(), user.title,
        "user title is rendered");

      assert.equal($('#test-mount .rank-posts-counted .stat-value').text(), 42,
        "user score is rendered");

      done();
    });
  });

  it("renders", function(done) {
    let user = testUtils.mockUser();
    user.meta = {score: 42};
    user.title = "Lorem ipsum";
    user.status = {is_online: true};

    /* jshint ignore:start */
    testUtils.render(
      <ActivePoster user={user} rank={user.rank} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .list-group-item', function() {
      assert.ok(true, "component renders");

      assert.equal($('#test-mount .status-icon').text().trim(), 'lens',
        "status icon is rendered");

      assert.equal($('#test-mount .status-label').text().trim(), 'Online',
        "status label is rendered");

      assert.equal($('#test-mount .rank-name').text().trim(), user.rank.name,
        "rank name is rendered");

      assert.equal($('#test-mount .user-title').text().trim(), user.title,
        "user title is rendered");

      assert.equal($('#test-mount .rank-posts-counted .stat-value').text(), 42,
        "user score is rendered");

      done();
    });
  });
});

describe("Active Posters Loading", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ActivePostersLoading />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .active-posters.ui-preview', function() {
      assert.ok(true, "component renders");

      done();
    });
  });
});

describe("No Active Posters", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<NoActivePosters trackedPeriod="30" />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .active-posters-list p.lead', function() {
      assert.ok(true, "component renders");

      assert.equal($('#test-mount p.lead').text().trim(),
        "No users have posted any new messages during last 30 days.",
        "valid empty message was displayed");

      done();
    });
  });
});

describe("Active Posters Root", function() {
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
          component: "active-posters",
          name: "Active posters"
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
          meta: {score: 42},
          title: "Lorem ipsum",
          status: {is_online: true}
        }),
        testUtils.mockUser({
          id: 122,
          meta: {score: 36},
          status: {is_online: true}
        })
      ],
      tracked_period: 30,
      count: 2
    };

    $.mockjax({
      url: '/test-api/users/?list=active',
      status: 200,
      responseText: data
    });

    misago._context.USERS = data;

    /* jshint ignore:start */
    testUtils.render(
      <Root user={misago._context.user}
            users={data.results}
            tick={123}
            route={{extra: {name: "Active posters"}}} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .active-posters.ui-ready', function() {
      assert.ok(true, "component renders");

      done();
    });
  });

  it("loads", function(done) {
    let data = {
      results: [
        testUtils.mockUser({
          id: 123,
          meta: {score: 42},
          title: "Lorem ipsum",
          status: {is_online: true}
        }),
        testUtils.mockUser({
          id: 122,
          meta: {score: 36},
          status: {is_online: true}
        })
      ],
      tracked_period: 30,
      count: 2
    };

    $.mockjax({
      url: '/test-api/users/?list=active',
      status: 200,
      responseText: data
    });

    misago._context.USERS = data;

    /* jshint ignore:start */
    testUtils.render(
      <Root user={misago._context.user}
            users={[]}
            tick={123}
            route={{extra: {name: "Active posters"}}} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .active-posters.ui-ready', function() {
      assert.ok(true, "component renders");

      done();
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: '/test-api/users/?list=active',
      status: 500
    });

    /* jshint ignore:start */
    testUtils.render(
      <Root user={misago._context.user}
            users={[]}
            tick={123}
            route={{extra: {name: "Active posters"}}} />
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