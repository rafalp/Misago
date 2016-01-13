import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import Loader from 'misago/components/loader'; // jshint ignore:line

describe("Loader", function() {
  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <Loader />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    assert.ok($('#test-mount .loader .loader-spinning-wheel').length,
      "component renders");
  });
});
