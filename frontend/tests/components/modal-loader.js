import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ModalLoader from 'misago/components/modal-loader'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Modal Loader", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders', function() {
    /* jshint ignore:start */
    testUtils.render(<ModalLoader />);
    /* jshint ignore:end */

    assert.ok($('#test-mount .modal-loader').length,
      "component renders");
    assert.ok($('#test-mount .loader .loader-spinning-wheel').length,
      "component contains loader");
  });
});
