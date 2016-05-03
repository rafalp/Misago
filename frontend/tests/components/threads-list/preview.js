import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ListPreview from 'misago/components/threads-list/list/preview'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Threads List Preview", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(<ListPreview />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .threads-list.ui-preview', function() {
      assert.ok(true, "component renders");

      assert.equal($('#test-mount .list-group-item').length, 3,
        "threads list preview renders with three thread previews");

      assert.ok(!$('#test-mount .list-group-item').eq(0).hasClass('hidden-xs'),
        "first row is always displayed");

      assert.ok($('#test-mount .list-group-item').eq(1).hasClass('hidden-xs'),
        "second row is hidden on mobile");

      assert.ok($('#test-mount .list-group-item').eq(2).hasClass('hidden-xs'),
        "third row is hidden on mobile");

      done();
    });
  });
});
