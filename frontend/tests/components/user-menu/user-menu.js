import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import { UserMenu, UserNav, CompactUserNav } from 'misago/components/user-menu/user-nav'; // jshint ignore:line
import misago from 'misago/index';
import dropdown from 'misago/services/mobile-navbar-dropdown';
import store from 'misago/services/store';

describe("UserMenu", function() {
  beforeEach(function() {
    window.contextClear(misago);
    window.contextAuthenticated(misago);

    window.initEmptyStore(store);
    window.initDropdown(dropdown);

    /* jshint ignore:start */
    ReactDOM.render(
      <UserMenu user={misago._context.user} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
  });

  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    let element = $('#test-mount .dropdown-menu');
    assert.ok(element.length, "component renders");
  });
});

describe("UserNav", function() {
  beforeEach(function() {
    window.contextClear(misago);
    window.contextAuthenticated(misago);

    window.initEmptyStore(store);
    window.initDropdown(dropdown);

    /* jshint ignore:start */
    ReactDOM.render(
      <UserNav user={misago._context.user} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
  });

  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    let element = $('#test-mount .user-dropdown');
    assert.ok(element.length, "component renders");
  });
});

describe("CompactUserNav", function() {
  beforeEach(function() {
    window.contextClear(misago);
    window.contextAuthenticated(misago);

    store.constructor();
    store.addReducer('auth', function(state={}, action=null){
      if (action) {
        return state;
      }
    }, {
      'isAuthenticated': misago.get('isAuthenticated'),
      'isAnonymous': !misago.get('isAuthenticated'),

      'user': misago.get('user')
    });
    store.init();

    window.initDropdown(dropdown);

    /* jshint ignore:start */
    ReactDOM.render(
      <CompactUserNav user={misago._context.user} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
  });

  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    let element = $('#test-mount img.user-avatar');
    assert.ok(element.length, "component renders");
  });

  it('opens dropdown on click', function() {
    window.simulateClick('#test-mount button');

    let element = $('#dropdown-mount>.user-dropdown');
    assert.ok(element.length, "component opened dropdown");
  });
});
