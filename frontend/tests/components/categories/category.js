import assert from 'assert';
import moment from 'moment'; // jshint ignore:line
import React from 'react'; // jshint ignore:line
import Category from 'misago/components/categories/Category'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Categories List Category", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    let category = {
      "id": 3,
      "name": "Games",
      "description": null,
      "is_closed": false,
      "threads": 82,
      "posts": 1944,
      "last_post_on": moment(),
      "last_thread_title": "Nemo quibusdam sunt ab odit omnis totam.",
      "last_poster_name": "Raelyn",
      "css_class": "accent",
      "is_read": false,
      "subcategories": [],
      "absolute_url": "/categories/#games-3",
      "last_thread_url": "/not-yet-implemented/",
      "last_poster_url": "/user/raelyn-74/",
      "acl": {
        "can_browse": true,
        "can_see_all_threads": 1
      }
    };

    testUtils.render(<Category category={category} />);
    /* jshint ignore:end */

    let element = $('#test-mount .panel-category');

    assert.ok(element.length, "component renders");
    assert.ok(element.hasClass('panel-category-accent'),
      "component renders with custom css class");

    assert.ok(!element.find('.category-description').length,
      "category description is not displayed");

    assert.ok(!element.find('.category-subcategories').length,
      "category subcategories are not displayed");
  });

  it("renders description", function() {
    /* jshint ignore:start */
    let category = {
      "id": 3,
      "name": "Games",
      "description": {
        "plain": "Lorem ipsum dolor met this is test!",
        "html": "<p>Lorem ipsum dolor met this is test!</p>"
      },
      "is_closed": false,
      "threads": 82,
      "posts": 1944,
      "last_post_on": moment(),
      "last_thread_title": "Nemo quibusdam sunt ab odit omnis totam.",
      "last_poster_name": "Raelyn",
      "css_class": "accent",
      "is_read": false,
      "subcategories": [],
      "absolute_url": "/categories/#games-3",
      "last_thread_url": "/not-yet-implemented/",
      "last_poster_url": "/user/raelyn-74/",
      "acl": {
        "can_browse": true,
        "can_see_all_threads": 1
      }
    };

    testUtils.render(<Category category={category} />);
    /* jshint ignore:end */

    let element = $('#test-mount .panel-category');

    assert.ok(element.length, "component renders");
    assert.ok(element.hasClass('panel-category-accent'),
      "component renders with custom css class");

    assert.equal(element.find('.category-description p').text(),
      "Lorem ipsum dolor met this is test!",
      "category description is displayed");
  });

  it("renders subcategory", function() {
    /* jshint ignore:start */
    let category = {
      "id": 3,
      "name": "Games",
      "description": null,
      "is_closed": false,
      "threads": 82,
      "posts": 1944,
      "last_post_on": moment(),
      "last_thread_title": "Nemo quibusdam sunt ab odit omnis totam.",
      "last_poster_name": "Raelyn",
      "css_class": "accent",
      "is_read": false,
      "subcategories": [
        {
          "id": 5,
          "name": "Subcategory",
          "description": null,
          "is_closed": false,
          "threads": 82,
          "posts": 1944,
          "last_post_on": moment(),
          "last_thread_title": "Nemo quibusdam sunt ab odit omnis totam.",
          "last_poster_name": "Raelyn",
          "css_class": "subaccent",
          "is_read": false,
          "subcategories": [],
          "absolute_url": "/categories/#games-3",
          "last_thread_url": "/not-yet-implemented/",
          "last_poster_url": "/user/raelyn-74/",
          "acl": {
            "can_browse": true,
            "can_see_all_threads": 1
          }
        }
      ],
      "absolute_url": "/categories/#games-3",
      "last_thread_url": "/not-yet-implemented/",
      "last_poster_url": "/user/raelyn-74/",
      "acl": {
        "can_browse": true,
        "can_see_all_threads": 1
      }
    };

    testUtils.render(<Category category={category} />);
    /* jshint ignore:end */

    let element = $('#test-mount .panel-category .category-subcategory');

    assert.ok(element.length, "component renders subcategory");

    assert.ok(!element.find('.subcategory-description').length,
      "subcategory description is not displayed");

    assert.ok(element.hasClass('subcategory-subaccent'),
      "subcategory has custom css class");
  });

  it("renders subcategory with description", function() {
    /* jshint ignore:start */
    let category = {
      "id": 3,
      "name": "Games",
      "description": null,
      "is_closed": false,
      "threads": 82,
      "posts": 1944,
      "last_post_on": moment(),
      "last_thread_title": "Nemo quibusdam sunt ab odit omnis totam.",
      "last_poster_name": "Raelyn",
      "css_class": "accent",
      "is_read": false,
      "subcategories": [
        {
          "id": 5,
          "name": "Subcategory",
          "description": {
            "plain": "Lorem ipsum dolor met this is test!",
            "html": "<p>Lorem ipsum dolor met this is test!</p>"
          },
          "is_closed": false,
          "threads": 82,
          "posts": 1944,
          "last_post_on": moment(),
          "last_thread_title": "Nemo quibusdam sunt ab odit omnis totam.",
          "last_poster_name": "Raelyn",
          "css_class": "subaccent",
          "is_read": false,
          "subcategories": [],
          "absolute_url": "/categories/#games-3",
          "last_thread_url": "/not-yet-implemented/",
          "last_poster_url": "/user/raelyn-74/",
          "acl": {
            "can_browse": true,
            "can_see_all_threads": 1
          }
        }
      ],
      "absolute_url": "/categories/#games-3",
      "last_thread_url": "/not-yet-implemented/",
      "last_poster_url": "/user/raelyn-74/",
      "acl": {
        "can_browse": true,
        "can_see_all_threads": 1
      }
    };

    testUtils.render(<Category category={category} />);
    /* jshint ignore:end */

    let element = $('#test-mount .panel-category .category-subcategory');

    assert.ok(element.length, "component renders subcategory");

    assert.equal(element.find('.subcategory-description p').text(),
      "Lorem ipsum dolor met this is test!",
      "subcategory description is displayed");
  });

  it("renders subcategory with subcategory", function() {
    /* jshint ignore:start */
    let category = {
      "id": 3,
      "name": "Games",
      "description": null,
      "is_closed": false,
      "threads": 82,
      "posts": 1944,
      "last_post_on": moment(),
      "last_thread_title": "Nemo quibusdam sunt ab odit omnis totam.",
      "last_poster_name": "Raelyn",
      "css_class": "accent",
      "is_read": false,
      "subcategories": [
        {
          "id": 5,
          "name": "Subcategory",
          "description": null,
          "is_closed": false,
          "threads": 82,
          "posts": 1944,
          "last_post_on": moment(),
          "last_thread_title": "Nemo quibusdam sunt ab odit omnis totam.",
          "last_poster_name": "Raelyn",
          "css_class": null,
          "is_read": false,
          "subcategories": [
            {
              "id": 12,
              "name": "Subcategory",
              "description": null,
              "is_closed": false,
              "threads": 82,
              "posts": 1944,
              "last_post_on": moment(),
              "last_thread_title": "Nemo quibusdam sunt ab odit omnis totam.",
              "last_poster_name": "Raelyn",
              "css_class": "subsubaccent",
              "is_read": false,
              "subcategories": [],
              "absolute_url": "/categories/#games-3",
              "last_thread_url": "/not-yet-implemented/",
              "last_poster_url": "/user/raelyn-74/",
              "acl": {
                "can_browse": true,
                "can_see_all_threads": 1
              }
            }
          ],
          "absolute_url": "/categories/#games-3",
          "last_thread_url": "/not-yet-implemented/",
          "last_poster_url": "/user/raelyn-74/",
          "acl": {
            "can_browse": true,
            "can_see_all_threads": 1
          }
        }
      ],
      "absolute_url": "/categories/#games-3",
      "last_thread_url": "/not-yet-implemented/",
      "last_poster_url": "/user/raelyn-74/",
      "acl": {
        "can_browse": true,
        "can_see_all_threads": 1
      }
    };

    testUtils.render(<Category category={category} />);
    /* jshint ignore:end */

    let element = $('#test-mount .subcategory-subcategories');

    assert.equal(element.length, 1, "component renders subsubcategory");

    assert.ok(element.find('.subcategory-subsubaccent'),
      "subsubcategory has custom css class");
  });
});