import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Loader from 'misago/components/loader'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Loader", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders', function() {
    /* jshint ignore:start */
    testUtils.render(<Loader />);
    /* jshint ignore:end */

    assert.ok($('#test-mount .loader .loader-spinning-wheel').length,
      "component renders");
  });
});
