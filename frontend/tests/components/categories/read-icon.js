import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReadIcon from 'misago/components/categories/read-icon'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Categories List Category Read Icon", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("render read", function() {
    /* jshint ignore:start */
    let category = {
      is_read: true,
      is_closed: false
    };

    testUtils.render(<ReadIcon category={category} />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .read-status.item-read .material-icon').text(),
      'chat_bubble_outline',
      "proper icon is displayed");

    assert.equal($('#test-mount .read-status').attr('title'),
      "This category has no new posts.",
      "proper state description is displayed");
  });

  it("render unread", function() {
    /* jshint ignore:start */
    let category = {
      is_read: false,
      is_closed: false
    };

    testUtils.render(<ReadIcon category={category} />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .read-status.item-new .material-icon').text(),
      'chat_bubble',
      "proper icon is displayed");

    assert.equal($('#test-mount .read-status').attr('title'),
      "This category has new posts.",
      "proper state description is displayed");
  });

  it("render read (closed)", function() {
    /* jshint ignore:start */
    let category = {
      is_read: true,
      is_closed: true
    };

    testUtils.render(<ReadIcon category={category} />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .read-status.item-read .material-icon').text(),
      'lock_outline',
      "proper icon is displayed");

    assert.equal($('#test-mount .read-status').attr('title'),
      "This category has no new posts. (closed)",
      "proper state description is displayed");
  });

  it("render unread (closed)", function() {
    /* jshint ignore:start */
    let category = {
      is_read: false,
      is_closed: true
    };

    testUtils.render(<ReadIcon category={category} />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .read-status.item-new .material-icon').text(),
      'lock',
      "proper icon is displayed");

    assert.equal($('#test-mount .read-status').attr('title'),
      "This category has new posts. (closed)",
      "proper state description is displayed");
  });
});