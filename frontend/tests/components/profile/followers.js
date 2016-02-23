import assert from 'assert';
import moment from 'moment';
import React from 'react'; // jshint ignore:line
import Followers from 'misago/components/profile/followers'; // jshint ignore:line
import misago from 'misago/index';
import reducer from 'misago/reducers/users';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
/* jshint ignore:start */
let userMock = {
  id: 42,
  username: 'TestUser',
  avatar_hash: 'abcdfefa'
};
let profileMock = {
  id: 123,
  username: 'BobBoberson',
  avatar_hash: 'abcdfefa'
};
/* jshint ignore:end */

describe("User Profile Followers List", function() {
  beforeEach(function() {
    misago._context = {
      USERS_API: '/test-api/users/'
    };

    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    store.constructor();
    store.addReducer('users', reducer, []);
    store.init();
  });

  afterEach(function() {
    testUtils.unmountComponents();
    $.mockjax.clear();
  });

  it("preloads empty", function(done) {
    misago._context.PROFILE_FOLLOWERS = {
      count: 0,
      more: 0,
      page: 1,
      pages: 1,
      results: []
    };

    /* jshint ignore:start */
    testUtils.render(
      <Followers user={userMock}
                 profile={profileMock}
                 users={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount p.lead', function(element) {
      assert.ok(element.length, "element renders");

      assert.equal($('#test-mount h3').text(),
        "BobBoberson has 0 followers.",
        "component has valid header");

      assert.equal(element.text(), "BobBoberson has no followers.",
        "empty message was displayed");

      done();
    });
  });

  it("preloads empty (owned)", function(done) {
    misago._context.PROFILE_FOLLOWERS = {
      count: 0,
      more: 0,
      page: 1,
      pages: 1,
      results: []
    };

    /* jshint ignore:start */
    testUtils.render(
      <Followers user={Object.assign({}, userMock, {id: 123})}
                 profile={profileMock}
                 users={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount p.lead', function(element) {
      assert.ok(element.length, "element renders");

      assert.equal($('#test-mount h3').text(),
        "You have 0 followers.",
        "component has valid header");

      assert.equal(element.text(), "You have no followers.",
        "empty message was displayed");

      done();
    });
  });

  it("loads empty", function(done) {
    $.mockjax({
      url: '/test-api/users/?followers=123&name=&page=1',
      status: 200,
      responseText: {
        count: 0,
        more: 0,
        page: 1,
        pages: 1,
        results: []
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Followers user={userMock}
                 profile={profileMock}
                 users={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount p.lead', function(element) {
      assert.ok(element.length, "element renders");
      assert.equal(element.text(), "BobBoberson has no followers.",
        "empty message was displayed");

      done();
    });
  });

  it("loads empty (owned)", function(done) {
    $.mockjax({
      url: '/test-api/users/?followers=123&name=&page=1',
      status: 200,
      responseText: {
        count: 0,
        more: 0,
        page: 1,
        pages: 1,
        results: []
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Followers user={Object.assign({}, userMock, {id: 123})}
                 profile={profileMock}
                 users={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount p.lead', function(element) {
      assert.ok(element.length, "element renders");
      assert.equal(element.text(), "You have no followers.",
        "empty message was displayed");

      done();
    });
  });

  it("loads users list", function(done) {
    $.mockjax({
      url: '/test-api/users/?followers=123&name=&page=1',
      status: 200,
      responseText: {
        count: 5,
        more: 0,
        page: 1,
        pages: 1,
        results: [1, 2, 3, 4, 5].map(function(id) {
          return {
            id: id,
            username: 'BobBoberson' + id,
            avatar_hash: 'abcdfefa',
            joined_on: moment().format(),
            rank: {
              name: 'Test Rank',
              absolute_url: '/users/test-rank'
            }
          };
        })
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Followers user={userMock}
                 profile={profileMock}
                 users={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .users-cards-list.ui-ready', function() {
      assert.equal($('#test-mount h3').text(), "BobBoberson has 5 followers.",
        "component has valid header");

      assert.equal(store.getState().users.length, 5,
        "component renders with five items");

      done();
    });
  });

  it("loads more changes", function(done) {
    $.mockjax({
      url: '/test-api/users/?followers=123&name=&page=1',
      status: 200,
      responseText: {
        count: 10,
        more: 5,
        page: 1,
        pages: 2,
        results: [1, 2, 3, 4, 5].map(function(id) {
          return {
            id: id,
            username: 'BobBoberson' + id,
            avatar_hash: 'abcdfefa',
            joined_on: moment().format(),
            rank: {
              name: 'Test Rank',
              absolute_url: '/users/test-rank'
            }
          };
        })
      }
    });

    $.mockjax({
      url: '/test-api/users/?followers=123&name=&page=2',
      status: 200,
      responseText: {
        count: 10,
        more: 0,
        page: 2,
        pages: 2,
        results: [1, 2, 3, 4, 5].map(function(id) {
          return {
            id: 5 + id,
            username: 'BobBoberson' + (5 + id),
            avatar_hash: 'abcdfefa',
            joined_on: moment().format(),
            rank: {
              name: 'Test Rank',
              absolute_url: '/users/test-rank'
            }
          };
        })
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Followers user={userMock}
                 profile={profileMock}
                 users={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .pager-more .btn', function() {
      assert.equal($('#test-mount h3').text(), "BobBoberson has 10 followers.",
        "component has valid header");

      testUtils.simulateClick('#test-mount .pager-more .btn');

      window.setTimeout(function() {
        assert.equal(store.getState().users.length, 10,
          "component renders with ten items");

        done();
      }, 300);
    });
  });

  it("loads search results", function(done) {
    $.mockjax({
      url: '/test-api/users/?followers=123&name=&page=1',
      status: 200,
      responseText: {
        count: 10,
        more: 5,
        page: 1,
        pages: 2,
        results: [1, 2, 3, 4, 5].map(function(id) {
          return {
            id: id,
            username: 'BobBoberson' + id,
            avatar_hash: 'abcdfefa',
            joined_on: moment().format(),
            rank: {
              name: 'Test Rank',
              absolute_url: '/users/test-rank'
            }
          };
        })
      }
    });

    $.mockjax({
      url: '/test-api/users/?followers=123&name=test&page=1',
      status: 200,
      responseText: {
        count: 3,
        more: 0,
        page: 1,
        pages: 1,
        results: [1, 2, 3].map(function(id) {
          return {
            id: 10 + id,
            username: 'BobBoberson' + (10 + id),
            avatar_hash: 'abcdfefa',
            joined_on: moment().format(),
            rank: {
              name: 'Test Rank',
              absolute_url: '/users/test-rank'
            }
          };
        })
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Followers user={userMock}
                 profile={profileMock}
                 users={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .pager-more .btn', function() {
      assert.equal($('#test-mount h3').text(),
        "BobBoberson has 10 followers.",
        "component has valid header");

      testUtils.simulateChange('#test-mount .form-control', 'test');

      window.setTimeout(function() {
        assert.equal(store.getState().users.length, 3,
          "component renders with three found items");

        assert.equal($('#test-mount h3').text(), "Found 3 users.",
          "component has valid header");

        done();
      }, 300);
    });
  });

  it("loads empty search results", function(done) {
    $.mockjax({
      url: '/test-api/users/?followers=123&name=&page=1',
      status: 200,
      responseText: {
        count: 10,
        more: 5,
        page: 1,
        pages: 2,
        results: [1, 2, 3, 4, 5].map(function(id) {
          return {
            id: id,
            username: 'BobBoberson' + id,
            avatar_hash: 'abcdfefa',
            joined_on: moment().format(),
            rank: {
              name: 'Test Rank',
              absolute_url: '/users/test-rank'
            }
          };
        })
      }
    });

    $.mockjax({
      url: '/test-api/users/?followers=123&name=test&page=1',
      status: 200,
      responseText: {
        count: 0,
        more: 0,
        page: 1,
        pages: 1,
        results: []
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Followers user={userMock}
                 profile={profileMock}
                 users={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .pager-more .btn', function() {
      assert.equal($('#test-mount h3').text(),
        "BobBoberson has 10 followers.",
        "component has valid header");

      testUtils.simulateChange('#test-mount .form-control', 'test');

      window.setTimeout(function() {
        assert.equal(store.getState().users.length, 0,
          "store is emptied");

        assert.equal($('#test-mount h3').text(), "Found 0 users.",
          "component has valid header");

        done();
      }, 300);
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: '/test-api/users/?followers=123&name=&page=1',
      status: 500
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Unknown error has occured.",
        type: 'error'
      }, "error message was shown");

      done();
    });

    /* jshint ignore:start */
    testUtils.render(
      <Followers user={userMock}
                 profile={profileMock}
                 users={[]} />
    );
    /* jshint ignore:end */
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: '/test-api/users/?followers=123&name=&page=1',
      status: 403,
      responseText: {
        detail: "You can't see it yo!"
      }
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "You can't see it yo!",
        type: 'error'
      }, "error message was shown");

      done();
    });

    /* jshint ignore:start */
    testUtils.render(
      <Followers user={userMock}
                 profile={profileMock}
                 users={[]} />
    );
    /* jshint ignore:end */
  });
});