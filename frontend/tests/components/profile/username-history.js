import assert from 'assert';
import moment from 'moment';
import React from 'react'; // jshint ignore:line
import UsernameHistory from 'misago/components/profile/username-history'; // jshint ignore:line
import misago from 'misago/index';
import reducer from 'misago/reducers/username-history';
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

describe("User Profile Username History", function() {
  beforeEach(function() {
    misago._context = {
      USERNAME_CHANGES_API: '/test-api/username-history/'
    };

    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    store.constructor();
    store.addReducer('username-history', reducer, []);
    store.init();
  });

  afterEach(function() {
    testUtils.unmountComponents();
    $.mockjax.clear();
  });

  it("preloads empty", function(done) {
    misago._context.PROFILE_NAME_HISTORY = {
      count: 0,
      more: 0,
      page: 1,
      pages: 1,
      results: []
    };

    /* jshint ignore:start */
    testUtils.render(
      <UsernameHistory user={userMock}
                       profile={profileMock}
                       username-history={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .ui-ready', function(element) {
      assert.ok(element.length, "element renders");

      assert.equal($('#test-mount h3').text(),
        "BobBoberson's username was changed 0 times.",
        "component has valid header");

      assert.equal(element.find('.empty-message').text(),
        "BobBoberson's username was never changed.",
        "empty message was displayed");

      done();
    });
  });

  it("preloads empty (owned)", function(done) {
    misago._context.PROFILE_NAME_HISTORY = {
      count: 0,
      more: 0,
      page: 1,
      pages: 1,
      results: []
    };

    /* jshint ignore:start */
    testUtils.render(
      <UsernameHistory user={Object.assign({}, userMock, {id: 123})}
                       profile={profileMock}
                       username-history={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .ui-ready', function(element) {
      assert.ok(element.length, "element renders");

      assert.equal($('#test-mount h3').text(),
        "Your username was changed 0 times.",
        "component has valid header");

      assert.equal(element.find('.empty-message').text(),
        "No name changes have been recorded for your account.",
        "empty message was displayed");

      done();
    });
  });

  it("loads empty", function(done) {
    $.mockjax({
      url: '/test-api/username-history/?user=123&search=&page=1',
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
      <UsernameHistory user={userMock}
                       profile={profileMock}
                       username-history={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .ui-ready', function(element) {
      assert.ok(element.length, "element renders");
      assert.equal(element.find('.empty-message').text(),
        "BobBoberson's username was never changed.",
        "empty message was displayed");

      done();
    });
  });

  it("loads empty (owned)", function(done) {
    $.mockjax({
      url: '/test-api/username-history/?user=123&search=&page=1',
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
      <UsernameHistory user={Object.assign({}, userMock, {id: 123})}
                       profile={profileMock}
                       username-history={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .ui-ready', function(element) {
      assert.ok(element.length, "element renders");
      assert.equal(element.find('.empty-message').text(),
        "No name changes have been recorded for your account.",
        "empty message was displayed");

      done();
    });
  });

  it("loads username changes", function(done) {
    $.mockjax({
      url: '/test-api/username-history/?user=123&search=&page=1',
      status: 200,
      responseText: {
        count: 5,
        more: 0,
        page: 1,
        pages: 1,
        results: [1, 2, 3, 4, 5].map(function(id) {
          return {
            id: id,
            changed_by: {
              id: 1,
              username: "rafalp",
              slug: "rafalp",
              avatar_hash: "5c6a04b4",
              absolute_url: "/user/rafalp-1/"
            },
            changed_by_username: "rafalp",
            changed_on: moment().format(),
            new_username: "Newt",
            old_username: "LoremIpsum"
          };
        })
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <UsernameHistory user={userMock}
                       profile={profileMock}
                       username-history={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .username-history.ui-ready', function() {
      assert.equal($('#test-mount h3').text(),
        "BobBoberson's username was changed 5 times.",
        "component has valid header");

      assert.equal(store.getState()['username-history'].length, 5,
        "component renders with five items");

      done();
    });
  });

  it("loads more changes", function(done) {
    $.mockjax({
      url: '/test-api/username-history/?user=123&search=&page=1',
      status: 200,
      responseText: {
        count: 10,
        more: 5,
        page: 1,
        pages: 2,
        results: [1, 2, 3, 4, 5].map(function(id) {
          return {
            id: id,
            changed_by: {
              id: 1,
              username: "rafalp",
              slug: "rafalp",
              avatar_hash: "5c6a04b4",
              absolute_url: "/user/rafalp-1/"
            },
            changed_by_username: "rafalp",
            changed_on: moment().format(),
            new_username: "Newt",
            old_username: "LoremIpsum"
          };
        })
      }
    });

    $.mockjax({
      url: '/test-api/username-history/?user=123&search=&page=2',
      status: 200,
      responseText: {
        count: 10,
        more: 0,
        page: 2,
        pages: 2,
        results: [1, 2, 3, 4, 5].map(function(id) {
          return {
            id: 5 + id,
            changed_by: {
              id: 1,
              username: "rafalp",
              slug: "rafalp",
              avatar_hash: "5c6a04b4",
              absolute_url: "/user/rafalp-1/"
            },
            changed_by_username: "rafalp",
            changed_on: moment().format(),
            new_username: "Newt",
            old_username: "LoremIpsum"
          };
        })
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <UsernameHistory user={userMock}
                       profile={profileMock}
                       username-history={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .pager-more .btn', function() {
      assert.equal($('#test-mount h3').text(),
        "BobBoberson's username was changed 10 times.",
        "component has valid header");

      testUtils.simulateClick('#test-mount .pager-more .btn');

      window.setTimeout(function() {
        assert.equal(store.getState()['username-history'].length, 10,
          "component renders with ten items");

        done();
      }, 300);
    });
  });

  it("loads search results", function(done) {
    $.mockjax({
      url: '/test-api/username-history/?user=123&search=&page=1',
      status: 200,
      responseText: {
        count: 10,
        more: 5,
        page: 1,
        pages: 2,
        results: [1, 2, 3, 4, 5].map(function(id) {
          return {
            id: id,
            changed_by: {
              id: 1,
              username: "rafalp",
              slug: "rafalp",
              avatar_hash: "5c6a04b4",
              absolute_url: "/user/rafalp-1/"
            },
            changed_by_username: "rafalp",
            changed_on: moment().format(),
            new_username: "Newt",
            old_username: "LoremIpsum"
          };
        })
      }
    });

    $.mockjax({
      url: '/test-api/username-history/?user=123&search=test&page=1',
      status: 200,
      responseText: {
        count: 3,
        more: 0,
        page: 1,
        pages: 1,
        results: [1, 2, 3].map(function(id) {
          return {
            id: 10 + id,
            changed_by: {
              id: 1,
              username: "rafalp",
              slug: "rafalp",
              avatar_hash: "5c6a04b4",
              absolute_url: "/user/rafalp-1/"
            },
            changed_by_username: "rafalp",
            changed_on: moment().format(),
            new_username: "Newt",
            old_username: "LoremIpsum"
          };
        })
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <UsernameHistory user={userMock}
                       profile={profileMock}
                       username-history={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .pager-more .btn', function() {
      assert.equal($('#test-mount h3').text(),
        "BobBoberson's username was changed 10 times.",
        "component has valid header");

      testUtils.simulateChange('#test-mount .form-control', 'test');

      window.setTimeout(function() {
        assert.equal(store.getState()['username-history'].length, 3,
          "component renders with three found items");

        assert.equal($('#test-mount h3').text(), "Found 3 username changes.",
          "component has valid header");

        done();
      }, 300);
    });
  });

  it("loads empty search results", function(done) {
    $.mockjax({
      url: '/test-api/username-history/?user=123&search=&page=1',
      status: 200,
      responseText: {
        count: 10,
        more: 5,
        page: 1,
        pages: 2,
        results: [1, 2, 3, 4, 5].map(function(id) {
          return {
            id: id,
            changed_by: {
              id: 1,
              username: "rafalp",
              slug: "rafalp",
              avatar_hash: "5c6a04b4",
              absolute_url: "/user/rafalp-1/"
            },
            changed_by_username: "rafalp",
            changed_on: moment().format(),
            new_username: "Newt",
            old_username: "LoremIpsum"
          };
        })
      }
    });

    $.mockjax({
      url: '/test-api/username-history/?user=123&search=test&page=1',
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
      <UsernameHistory user={userMock}
                       profile={profileMock}
                       username-history={[]} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .pager-more .btn', function() {
      assert.equal($('#test-mount h3').text(),
        "BobBoberson's username was changed 10 times.",
        "component has valid header");

      testUtils.simulateChange('#test-mount .form-control', 'test');

      window.setTimeout(function() {
        assert.equal(store.getState()['username-history'].length, 0,
          "store is emptied");

        assert.equal($('#test-mount h3').text(), "Found 0 username changes.",
          "component has valid header");

        done();
      }, 300);
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: '/test-api/username-history/?user=123&search=&page=1',
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
      <UsernameHistory user={userMock}
                       profile={profileMock}
                       username-history={[]} />
    );
    /* jshint ignore:end */
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: '/test-api/username-history/?user=123&search=&page=1',
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
      <UsernameHistory user={userMock}
                       profile={profileMock}
                       username-history={[]} />
    );
    /* jshint ignore:end */
  });
});