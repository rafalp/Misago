import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import ReactTestUtils from 'react-addons-test-utils';
import { CompactGuestNav } from 'misago/components/user-menu/guest-nav'; // jshint ignore:line
import dropdown from 'misago/services/mobile-navbar-dropdown';
import store from 'misago/services/store';

describe("CompactGuestNav", function() {
  beforeEach(function() {
    window.initEmptyStore(store);
    window.initDropdown(dropdown);
  });

  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <CompactGuestNav />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount img.user-avatar');
    assert.ok(element.length, "component renders");
  });

  it('opens dropdown on click', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <CompactGuestNav />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    ReactTestUtils.Simulate.click($('#test-mount button').get(0));

    let element = $('#dropdown-mount>.dropdown-menu');
    assert.ok(element.length, "component opened dropdown");
  });
});
