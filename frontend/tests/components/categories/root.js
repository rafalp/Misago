import assert from 'assert';
import React from 'react'; // jshint ignore:line
import CategoriesList from 'misago/components/categories/root'; // jshint ignore:line
import misago from 'misago/index';
import ajax from 'misago/services/ajax';
import polls from 'misago/services/polls';
import snackbar from 'misago/services/snackbar';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
let categories = [
  {
    "id": 3,
    "name": "Games",
    "description": null,
    "is_closed": false,
    "threads": 82,
    "posts": 1944,
    "last_post_on": "2016-02-25T21:15:53.231778Z",
    "last_thread_title": "Nemo quibusdam sunt ab odit omnis totam.",
    "last_poster_name": "Raelyn",
    "css_class": "accent",
    "is_read": false,
    "subcategories": [],
    "absolute_url": "/category/games-3/",
    "last_thread_url": "/thread/test-thread-132/",
    "last_post_url": "/thread/test-thread-132/last/",
    "last_poster_url": "/user/raelyn-74/",
    "acl": {
      "can_browse": true,
      "can_see_all_threads": 1
    }
  },
  {
    "id": 4,
    "name": "Second category",
    "description": {
      "plain": "Lorem ipsum dolor met sit amet elit.",
      "html": "<p>Lorem ipsum dolor met sit amet elit.</p>"
    },
    "is_closed": false,
    "threads": 418,
    "posts": 7741,
    "last_post_on": "2016-02-25T21:15:54.483911Z",
    "last_thread_title": "Iste officiis debitis velit non magnam aut a.",
    "last_poster_name": "Myrna",
    "css_class": "",
    "is_read": false,
    "subcategories": [
      {
        "id": 5,
        "name": "Action",
        "description": {
          "plain": "Lorem ipsum dolor met sit amet elit pacem bellum sequor.",
          "html": "<p>Lorem ipsum dolor met sit amet elit pacem bellum sequor.</p>"
        },
        "is_closed": true,
        "threads": 263,
        "posts": 5386,
        "last_post_on": "2016-02-25T21:15:54.483911Z",
        "last_thread_title": "Iste officiis debitis velit non magnam aut a.",
        "last_poster_name": "Myrna",
        "css_class": "",
        "is_read": false,
        "subcategories": [
          {
            "id": 7,
            "name": "Multiplayer",
            "description": null,
            "is_closed": false,
            "threads": 95,
            "posts": 1567,
            "last_post_on": "2016-02-25T21:15:53.697017Z",
            "last_thread_title": "Et debitis unde in eius.",
            "last_poster_name": "Morton",
            "css_class": "",
            "is_read": false,
            "subcategories": [],
            "absolute_url": "/category/multiplayer-7/",
            "last_thread_url": "/thread/test-thread-134/",
            "last_post_url": "/thread/test-thread-134/last/",
            "last_poster_url": "/user/morton-30/",
            "acl": {
              "can_browse": true,
              "can_see_all_threads": 1
            }
          },
          {
            "id": 8,
            "name": "Single player",
            "description": null,
            "is_closed": false,
            "threads": 93,
            "posts": 2422,
            "last_post_on": "2016-02-25T21:15:54.483911Z",
            "last_thread_title": "Iste officiis debitis velit non magnam aut a.",
            "last_poster_name": "Myrna",
            "css_class": "",
            "is_read": false,
            "subcategories": [],
            "absolute_url": "/category/single-player-8/",
            "last_thread_url": "/thread/test-thread-135/",
            "last_post_url": "/thread/test-thread-135/last/",
            "last_poster_url": "/user/myrna-18/",
            "acl": {
              "can_browse": true,
              "can_see_all_threads": 1
            }
          }
        ],
        "absolute_url": "/category/action-5/",
        "last_thread_url": "/thread/test-thread-136/",
        "last_post_url": "/thread/test-thread-136/last/",
        "last_poster_url": "/user/myrna-52/",
        "acl": {
          "can_browse": true,
          "can_see_all_threads": 1
        }
      },
      {
        "id": 6,
        "name": "Sandbox",
        "description": null,
        "is_closed": false,
        "threads": 73,
        "posts": 979,
        "last_post_on": "2016-02-25T21:15:54.240616Z",
        "last_thread_title": "Totam hic excepturi nulla asperiores illum.",
        "last_poster_name": "Camille",
        "css_class": "",
        "is_read": false,
        "subcategories": [],
        "absolute_url": "/category/sandbox-6/",
        "last_thread_url": "/thread/test-thread-137/",
        "last_post_url": "/thread/test-thread-137/last/",
        "last_poster_url": "/user/camille-29/",
        "acl": {
          "can_browse": true,
          "can_see_all_threads": 1
        }
      }
    ],
    "absolute_url": "/category/second-category-4/",
    "last_thread_url": "/thread/test-thread-133/",
    "last_post_url": "/thread/test-thread-133/last/",
    "last_poster_url": "/user/myrna-88/",
    "acl": {
      "can_browse": true,
      "can_see_all_threads": 1
    }
  }
];

describe("Categories List", function() {
  beforeEach(function() {
    misago._context = {
      CATEGORIES: categories,
      CATEGORIES_API: '/test-api/categories/',
      CATEGORIES_ON_INDEX: false
    };

    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    polls.init(ajax, snackbar);
  });

  afterEach(function() {
    polls.stop('categories');
    testUtils.unmountComponents();
    $.mockjax.clear();
  });

  it("renders and loads", function(done) {
    $.mockjax({
      url: '/test-api/categories/',
      status: 200,
      responseText: categories
    });

    /* jshint ignore:start */
    testUtils.render(<CategoriesList />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .panel-category').length, 2,
      "two categories rendered initially");

    window.setTimeout(function() {
      let element = $('#test-mount .categories-list');
      assert.ok(element.length, "component renders");

      assert.equal(element.find('.panel-category').length, 2,
        "two categories rendered");

      done();
    }, 200);
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: '/test-api/categories/',
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
    testUtils.render(<CategoriesList />);
    /* jshint ignore:end */
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: '/test-api/categories/',
      status: 403,
      responseText: {
        detail: "You can't see it yo!"
      }
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "You can't see it yo!",
        type: 'error'
      }, "backend returned error message was shown");

      done();
    });

    /* jshint ignore:start */
    testUtils.render(<CategoriesList />);
    /* jshint ignore:end */
  });
});
