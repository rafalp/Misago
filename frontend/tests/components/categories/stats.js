import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Stats from 'misago/components/categories/stats'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Categories List Category Stats", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders with zeros", function() {
    /* jshint ignore:start */
    let category = {
      threads: 0,
      posts: 0
    };

    testUtils.render(<Stats category={category} />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .category-threads').text(), "0 threads",
      "proper threads count is displayed");

    assert.equal($('#test-mount .category-posts').text(), "0 posts",
      "proper threads count is displayed");
  });

  it("renders with threads", function() {
    /* jshint ignore:start */
    let category = {
      threads: 123,
      posts: 0
    };

    testUtils.render(<Stats category={category} />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .category-threads').text(), "123 threads",
      "proper threads count is displayed");

    assert.equal($('#test-mount .category-posts').text(), "0 posts",
      "proper threads count is displayed");
  });

  it("renders with posts", function() {
    /* jshint ignore:start */
    let category = {
      threads: 0,
      posts: 123
    };

    testUtils.render(<Stats category={category} />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .category-threads').text(), "0 threads",
      "proper threads count is displayed");

    assert.equal($('#test-mount .category-posts').text(), "123 posts",
      "proper threads count is displayed");
  });

  it("renders with threads and posts", function() {
    /* jshint ignore:start */
    let category = {
      threads: 1,
      posts: 4
    };

    testUtils.render(<Stats category={category} />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .category-threads').text(), "1 thread",
      "proper threads count is displayed");

    assert.equal($('#test-mount .category-posts').text(), "4 posts",
      "proper threads count is displayed");
  });
});