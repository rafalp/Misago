import assert from 'assert';
import React from 'react'; // jshint ignore:line
import EmptyMessage from 'misago/components/categories/empty-message'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Categories List Empty Message", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    testUtils.render(<EmptyMessage />);
    /* jshint ignore:end */

    assert.equal($('#test-mount .material-icon').text(), 'info_outline',
      "proper icon is displayed");

    assert.equal($('#test-mount p.lead').text(),
      "No categories are available.",
      "proper message is displayed");
  });
});