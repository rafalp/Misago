import assert from 'assert';
import React from 'react'; // jshint ignore:line
import store from 'misago/services/store';
import { MobileNavbarDropdown } from 'misago/services/mobile-navbar-dropdown';
import * as testUtils from 'misago/utils/test-utils';

var dropdown = null;

class TestComponentA extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="dropdown-a">
      <p>This is first test dropdown!</p>
    </div>;
    /* jshint ignore:end */
  }
}

class TestComponentB extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="dropdown-b">
      <p>This is second test dropdown!</p>
    </div>;
    /* jshint ignore:end */
  }
}

describe("Dropdown", function() {
  beforeEach(function() {
    dropdown = new MobileNavbarDropdown();
    dropdown.init(document.getElementById('dropdown-mount'));

    store.constructor();
    store.addReducer('test', function(state={}, action=null) { return {}; }, {}); // jshint ignore:line
    store.init();
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('shows component', function(done) {
    dropdown.show(TestComponentA);

    window.setTimeout(function() {
      let element = $('#dropdown-mount .dropdown-a');
      assert.ok(element.length, "component was rendered");
      done();
    }, 100);
  });

  it('shows and cycles component', function(done) {
    dropdown.show(TestComponentA);

    window.setTimeout(function() {
      let element = $('#dropdown-mount .dropdown-a');
      assert.ok(element.length, "component was rendered");

      dropdown.show(TestComponentB);
    }, 100);

    window.setTimeout(function() {
      let element = $('#dropdown-mount .dropdown-b');
      assert.ok(element.length, "component was toggled");
      done();
    }, 300);
  });
});
