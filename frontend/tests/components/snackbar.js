import assert from 'assert';
import React from 'react'; // jshint ignore:line
import { Snackbar } from 'misago/components/snackbar'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Snackbar", function() {
  afterEach(function() {
    testUtils.emptyTestContainers();
  });

  it('renders', function() {
    /* jshint ignore:start */
    testUtils.render(<Snackbar isVisible={false} message="" type="info" />);
    /* jshint ignore:end */

    assert.ok($('.alerts-snackbar').hasClass('out'), "component is hidden");

    /* jshint ignore:start */
    testUtils.render(
      <Snackbar isVisible={true} type="success"
                message="Lorem ipsum dolor met." />
    );
    /* jshint ignore:end */

    assert.ok($('.alerts-snackbar').hasClass('in'), "component is visible");
    assert.ok($('.alerts-snackbar p').hasClass('alert-success'),
      "component has alert-success class");

    assert.equal(
      $.trim($('.alerts-snackbar p').text()), "Lorem ipsum dolor met.",
      "message is inserted");

    /* jshint ignore:start */
    testUtils.render(
      <Snackbar isVisible={true} type="info"
                message="Lorem ipsum dolor met." />
    );
    /* jshint ignore:end */
    assert.ok($('.alerts-snackbar p').hasClass('alert-info'),
      "component has alert-info class");

    /* jshint ignore:start */
    testUtils.render(
      <Snackbar isVisible={true} type="warning"
                message="Lorem ipsum dolor met." />
    );
    /* jshint ignore:end */
    assert.ok($('.alerts-snackbar p').hasClass('alert-warning'),
      "component has alert-warning class");

    /* jshint ignore:start */
    testUtils.render(
      <Snackbar isVisible={true} type="error"
                message="Lorem ipsum dolor met." />
    );
    /* jshint ignore:end */
    assert.ok($('.alerts-snackbar p').hasClass('alert-danger'),
      "component has alert-danger class");
  });
});
