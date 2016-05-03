import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ListEmpty from 'misago/components/threads-list/list/empty'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Empty Threads List Preview", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <ListEmpty diffSize={0}>
        <p>Well, this is empty list message!</p>
      </ListEmpty>
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .threads-list p', function(element) {
      assert.ok(true, "component renders");

      assert.equal($(element).text(), "Well, this is empty list message!",
        "empty list renders its child content as empty message");

      assert.ok(!$(element).find('.threads-diff-message').length,
        "message about new threads is hidden");

      done();
    });
  });

  it("renders with diff message", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    const applyDiff = function() {
      assert.ok(true, "apply diff message runs callback");

      done();
    };

    testUtils.render(
      <ListEmpty applyDiff={applyDiff} diffSize={1}>
        <p>Well, this is empty list message!</p>
      </ListEmpty>
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .threads-list .btn', function(element) {
      assert.ok(true, "component renders");

      assert.equal($(element).find('.diff-message').text(),
        "There is 1 new or updated thread. Click this message to show it.",
        "message about new threads is displayed");

      testUtils.simulateClick('.btn');
    });
  });
});
