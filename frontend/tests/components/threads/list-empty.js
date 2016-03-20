import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ListEmpty from 'misago/components/threads/list-empty'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Threads List Empty Message", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders general message", function() {
    /* jshint ignore:start */
    testUtils.render(
      <ListEmpty category={{special_role: true}}
                 list={{type: 'all'}} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .empty-message .lead');
    assert.ok(element.length, "component renders");
    assert.equal(element.text(), "There are no threads on this forum... yet!",
      "general message was displayed");
  });

  it("renders category message", function() {
    /* jshint ignore:start */
    testUtils.render(<ListEmpty category={{}} list={{type: 'all'}} />);
    /* jshint ignore:end */

    let element = $('#test-mount .empty-message .lead');
    assert.ok(element.length, "component renders");
    assert.equal(element.text(), "There are no threads in this category.",
      "category message was displayed");
  });

  it("renders list message", function() {
    /* jshint ignore:start */
    testUtils.render(<ListEmpty category={{}} list={{type: 'other'}} />);
    /* jshint ignore:end */

    let element = $('#test-mount .empty-message');
    assert.ok(element.length, "component renders");
    assert.equal(element.text(),
      "No threads matching specified criteria were found.",
      "list message was displayed");
  });
});
