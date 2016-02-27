import assert from 'assert';
import moment from 'moment';
import React from 'react'; // jshint ignore:line
import LastActivity from 'misago/components/categories/last-activity'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Categories List Category Last Activity", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders category protected message", function() {
    /* jshint ignore:start */
    let category = {
      acl: {
        can_browse: false
      }
    };

    testUtils.render(<LastActivity category={category} />);
    /* jshint ignore:end */

    let element = $('#test-mount .thread-message');

    assert.ok(element.text().indexOf("category is protected") !== 1,
      "category is protected message is displayed");
    assert.equal(element.find('.material-icon').text(), 'highlight_off',
      "proper icon is used");
  });

  it("renders category private message", function() {
    /* jshint ignore:start */
    let category = {
      acl: {
        can_browse: true,
        can_see_all_threads: false
      }
    };

    testUtils.render(<LastActivity category={category} />);
    /* jshint ignore:end */

    let element = $('#test-mount .thread-message');

    assert.ok(element.text().indexOf("category is private") !== 1,
      "category is private message is displayed");
    assert.equal(element.find('.material-icon').text(), 'info_outline',
      "proper icon is used");
  });

  it("renders category empty message", function() {
    /* jshint ignore:start */
    let category = {
      last_thread_title: null,

      acl: {
        can_browse: true,
        can_see_all_threads: true
      }
    };

    testUtils.render(<LastActivity category={category} />);
    /* jshint ignore:end */

    let element = $('#test-mount .thread-message');

    assert.ok(element.text().indexOf("category is empty") !== 1,
      "category is empty message is displayed");
    assert.equal(element.find('.material-icon').text(), 'error_outline',
      "proper icon is used");
  });

  it("renders guest-posted thread", function() {
    let category = {
      last_thread_title: "Misago Test Thread",
      last_thread_url: '/test-thread/url-123/',

      last_poster_name: 'BobBoberson',
      last_poster_url: null,

      last_post_on: moment().subtract(3, 'days'),

      acl: {
        can_browse: true,
        can_see_all_threads: true
      }
    };

    /* jshint ignore:start */
    testUtils.render(<LastActivity category={category} />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .thread-title a').attr('href'),
      category.last_thread_url,
      "thread url is displayed");

    assert.equal($('#test-mount .thread-title a').text(),
      category.last_thread_title,
      "thread name is displayed");

    assert.equal($('#test-mount .poster-name span.item-title').text(),
      category.last_poster_name,
      "non-anchor poster name is displayed");

    assert.equal($('#test-mount .thread-date abbr').text(),
      "3 days ago",
      "last post date is displayed");
  });

  it("renders thread", function() {
    let category = {
      last_thread_title: "Misago Test Thread",
      last_thread_url: '/test-thread/url-123/',

      last_poster_name: 'BobBoberson',
      last_poster_url: '/user/bobberson-13213/',

      last_post_on: moment().subtract(3, 'days'),

      acl: {
        can_browse: true,
        can_see_all_threads: true
      }
    };

    /* jshint ignore:start */
    testUtils.render(<LastActivity category={category} />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .thread-title a').attr('href'),
      category.last_thread_url,
      "thread url is displayed");

    assert.equal($('#test-mount .thread-title a').text(),
      category.last_thread_title,
      "thread name is displayed");

    assert.equal($('#test-mount .poster-name a.item-title').attr('href'),
      category.last_poster_url,
      "url to poster's profile is displayed");

    assert.equal($('#test-mount .poster-name a.item-title').text(),
      category.last_poster_name,
      "non-anchor poster name is displayed");

    assert.equal($('#test-mount .thread-date abbr').text(),
      "3 days ago",
      "last post date is displayed");
  });
});