import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import { Snackbar } from 'misago/components/snackbar'; // jshint ignore:line

describe("Snackbar", function() {
  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <Snackbar isVisible={false} message="" type="info" />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    assert.ok($('.alerts-snackbar').hasClass('out'), "component is hidden");

    /* jshint ignore:start */
    ReactDOM.render(
      <Snackbar isVisible={true} type="success"
                message="Lorem ipsum dolor met." />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    assert.ok($('.alerts-snackbar').hasClass('in'), "component is visible");
    assert.ok($('.alerts-snackbar p').hasClass('alert-success'),
      "component has alert-success class");

    assert.equal(
      $.trim($('.alerts-snackbar p').text()), "Lorem ipsum dolor met.",
      "message is inserted");

    /* jshint ignore:start */
    ReactDOM.render(
      <Snackbar isVisible={true} type="info"
                message="Lorem ipsum dolor met." />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
    assert.ok($('.alerts-snackbar p').hasClass('alert-info'),
      "component has alert-info class");

    /* jshint ignore:start */
    ReactDOM.render(
      <Snackbar isVisible={true} type="warning"
                message="Lorem ipsum dolor met." />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
    assert.ok($('.alerts-snackbar p').hasClass('alert-warning'),
      "component has alert-warning class");

    /* jshint ignore:start */
    ReactDOM.render(
      <Snackbar isVisible={true} type="error"
                message="Lorem ipsum dolor met." />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
    assert.ok($('.alerts-snackbar p').hasClass('alert-danger'),
      "component has alert-danger class");
  });
});
