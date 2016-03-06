import assert from 'assert';
import React from 'react'; // jshint ignore:line
import DropdownToggle from 'misago/components/dropdown-toggle'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Dropdown Toggle", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders', function() {
    /* jshint ignore:start */
    testUtils.render(<DropdownToggle />);
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component rendered");
    assert.equal(element.attr('type'), 'button', "component is regular button");
  });

  it('handles clicks', function(done) { // jshint ignore:line
    /* jshint ignore:start */
    function click() {
      assert.ok(true, "component called callback on click");
      done();
    }

    testUtils.render(<DropdownToggle toggleNav={click} />);
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component rendered");
    assert.equal(element.attr('type'), 'button', "component is regular button");
    testUtils.simulateClick('#test-mount button');
  });

  it('renders open', function() {
    /* jshint ignore:start */
    testUtils.render(<DropdownToggle dropdown={true} />);
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.hasClass('open'), "button has open class");
    assert.equal(element.attr('aria-expanded'), 'true',
      "aria-expanded is set to true");
  });
});
