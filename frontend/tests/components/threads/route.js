import assert from 'assert';
import moment from 'moment'; // jshint ignore:line
import React from 'react'; // jshint ignore:line
import Route from 'misago/components/threads/route'; // jshint ignore:line
import misago from 'misago/index';
import reducer, { hydrateThread } from 'misago/reducers/threads'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import title from 'misago/services/page-title';
import polls from 'misago/services/polls';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
/* jshint ignore:start */
let route = {
  'lists': [
    {
      type: 'all',
      path: '',
      name: "All",
      longName: "All threads"
    },
    {
      type: 'my',
      path: 'my/',
      name: "My",
      longName: "My threads"
    },
    {
      type: 'new',
      path: 'new/',
      name: "New",
      longName: "New threads"
    },
    {
      type: 'unread',
      path: 'unread/',
      name: "Unread",
      longName: "Unread threads"
    },
    {
      type: 'subscribed',
      path: 'subscribed/',
      name: "Subscribed",
      longName: "Subscribed threads"
    }
  ],
  list: {
    type: 'all',
    path: '',
    name: "All",
    longName: "All threads"
  },
  categoriesMap: {
    1: {
      id: 1,
      parent: null,
      name: "Lorem",
      description: {
        plain: "Lorem ipsum dolor met sit amet eli.",
        html: "<p>Lorem ipsum dolor met sit amet eli.</p>"
      },
      css_class: null,
      absolute_url: '/categories/category-1/'
    },
    2: {
      id: 2,
      parent: null,
      name: "Ipsum",
      description: {
        plain: "Lorem ipsum dolor met sit amet eli.",
        html: "<p>Lorem ipsum dolor met sit amet eli.</p>"
      },
      css_class: null,
      absolute_url: '/categories/category-2/'
    },
    3: {
      id: 3,
      parent: null,
      name: "Dolor met",
      description: {
        plain: "Lorem ipsum dolor met sit amet eli.",
        html: "<p>Lorem ipsum dolor met sit amet eli.</p>"
      },
      css_class: null,
      absolute_url: '/categories/category-3/'
    }
  },
  category: {
    id: 1,
    parent: null,
    name: "Lorem",
    description: {
      plain: "Lorem ipsum dolor met sit amet eli.",
      html: "<p>Lorem ipsum dolor met sit amet eli.</p>"
    },
    css_class: null,
    absolute_url: '/categories/category-1/'
  }
};

let user = {
  id: null
};
/* jshint ignore:end */
let thread = {
  id: 1,
  title: "Test thread",
  category: 3,
  top_category: 1,
  started_on: moment().format(),
  last_post: 3,
  last_post_url: '/thread/test-thread-132/last/',
  last_poster_name: 'BobBoberson',
  last_poster_url: null,
  last_post_on: moment().format(),
  is_read: true,
  acl: {},
};

describe("Threads List Route", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    polls.init(ajax, snackbar);

    misago._context = {
      CATEGORIES_ON_INDEX: false,
      THREADS_API: '/test-api/threads/',

      SETTINGS: {
        forum_name: "Test Forum",
        forum_index_title: "Forum Index"
      }
    };

    store.constructor();
    store.addReducer('threads', reducer, []);
    store.addReducer('tick', function(state, action) {
      if (action || true) {
        return {'tick': 123};
      }
    }, {});

    store.init();

    title.init(
      misago._context.SETTINGS.forum_index_title,
      misago._context.SETTINGS.forum_name);
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("inits with preloaded data", function(done) {
    misago._context.THREADS = {
      results: [],

      count: 1,
      more: 0,

      page: 1,
      pages: 1,

      subcategories: [2, 3]
    };

    $.mockjax({
      url: '/test-api/threads/?category=1&list=all&page=1',
      status: 200,
      responseText: {
        results: [],

        count: 1,
        more: 0,

        page: 1,
        pages: 1,

        subcategories: [2]
      }
    });

    /* jshint ignore:start */
    let threads = [
      hydrateThread(thread)
    ];
    testUtils.render(
      <Route route={route} selection={[]} threads={threads} user={user} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .thread-title', function(element) {
      assert.equal($('.threads-list .item-read').length, 1,
        "one thread was rendered");

      assert.equal($('.page-header h1').text(), "Lorem",
        "category name is shown in header");

      assert.equal($('.category-description .lead p').text(),
        "Lorem ipsum dolor met sit amet eli.",
        "category description was displayed");

      assert.equal($('.category-picker li').length, 2,
        "categories picker shows two cats");

      assert.equal(document.title, "Lorem | Test Forum",
        "valid page title is set");

      assert.equal(element.text(), "Test thread", "test thread was displayed");

      assert.ok(!$('.pager-more').length, "load more button is hidden");

      done();
    });
  });

  it("loads data", function(done) {
    $.mockjax({
      url: '/test-api/threads/?category=1&list=all&page=1',
      status: 200,
      responseText: {
        results: [thread],

        count: 1,
        more: 0,

        page: 1,
        pages: 1,

        subcategories: [2]
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Route route={route} selection={[]} threads={[]} user={user} />
    );
    /* jshint ignore:end */

    window.setTimeout(function() {
      let state = store.getState().threads;
      assert.equal(state.length, 1, "one thread was loaded into store");
      assert.equal(state[0].title, "Test thread", "test thread was loaded");

      assert.equal($('.category-picker li').length, 1,
        "categories picker shows one category");

      done();
    } , 300);
  });

  it("loads empty", function(done) {
    $.mockjax({
      url: '/test-api/threads/?category=1&list=all&page=1',
      status: 200,
      responseText: {
        results: [],

        count: 0,
        more: 0,

        page: 1,
        pages: 1,

        subcategories: []
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Route route={route} selection={[]} threads={[]} user={user} />
    );
    /* jshint ignore:end */

    window.setTimeout(function() {
      let state = store.getState().threads;
      assert.equal(state.length, 0, "no threads were loaded into store");

      assert.equal($('.category-picker li').length, 0,
        "categories picker is empty");

      done();
    } , 300);
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: '/test-api/threads/?category=1&list=all&page=1',
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
      <Route route={route} selection={[]} threads={[]} user={user} />
    );
    /* jshint ignore:end */
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: '/test-api/threads/?category=1&list=all&page=1',
      status: 403,
      responseText: {
        detail: "Nope, can't show you that."
      }
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Nope, can't show you that.",
        type: 'error'
      }, "error message was shown");

      done();
    });

    /* jshint ignore:start */
    testUtils.render(
      <Route route={route} selection={[]} threads={[]} user={user} />
    );
    /* jshint ignore:end */
  });

  it("loads additional threads", function(done) {
    $.mockjax({
      url: '/test-api/threads/?category=1&list=all&page=1',
      status: 200,
      responseText: {
        results: [thread],

        count: 1,
        more: 1,

        page: 1,
        pages: 2,

        subcategories: []
      }
    });

    $.mockjax({
      url: '/test-api/threads/?category=1&list=all&page=2',
      status: 200,
      responseText: {
        results: [Object.assign({}, thread, {
          id: 2,
          title: "Other thread",
          last_post: 2
        })],

        count: 1,
        more: 0,

        page: 2,
        pages: 2,

        subcategories: [1]
      }
    });

    /* jshint ignore:start */
    testUtils.render(
      <Route route={route} selection={[]} threads={[]} user={user} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .pager-more .btn', function() {
      assert.ok(true, "load more button is present");
      testUtils.simulateClick('#test-mount .pager-more .btn');

      window.setTimeout(function() {
        let state = store.getState().threads;
        assert.equal(state.length, 2, "two thread were loaded into store");
        assert.equal(state[0].title, "Test thread", "test thread was loaded");
        assert.equal(state[1].title, "Other thread", "new thread was added");

        assert.equal($('.category-picker li').length, 1,
          "categories picker shows one category");

        done();
      } , 300);
    });
  });

  it("renders for forum index", function(done) {
    $.mockjax({
      url: '/test-api/threads/?category=&list=all&page=1',
      status: 200,
      responseText: {
        results: [thread],

        count: 1,
        more: 0,

        page: 1,
        pages: 1,

        subcategories: [2]
      }
    });

    /* jshint ignore:start */
    let finalRoute = Object.assign({}, route, {
      category: Object.assign({}, route.category, {
        special_role: true
      })
    });
    testUtils.render(
      <Route route={finalRoute} selection={[]} threads={[]} user={user} />
    );
    /* jshint ignore:end */

    window.setTimeout(function() {
      assert.equal($('.page-header h1').text(), "Forum Index",
        "forum title is shown in header");
      assert.equal(document.title, "Forum Index",
        "valid page title is set");
      done();
    } , 300);
  });
});