import assert from 'assert';
import React from 'react'; // jshint ignore:line
import { GuestMenu, GuestNav, CompactGuestNav } from 'misago/components/user-menu/guest-nav'; // jshint ignore:line
import misago from 'misago/index';
import dropdown from 'misago/services/mobile-navbar-dropdown';
import modal from 'misago/services/modal';
import store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

describe("GuestMenu", function() {
  beforeEach(function() {
    testUtils.initEmptyStore(store);
    testUtils.initDropdown(dropdown);
    testUtils.initModal(modal);

    misago._context = {
      'FORGOTTEN_PASSWORD_URL': '/forgotten-password/'
    };

    /* jshint ignore:start */
    testUtils.render(<GuestMenu />);
    /* jshint ignore:end */
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders', function() {
    let element = $('#test-mount .dropdown-menu');
    assert.ok(element.length, "component renders");
  });

  it('opens sign in modal on click', function(done) {
    testUtils.simulateClick('#test-mount .btn-default');

    testUtils.onElement('#modal-mount .modal-sign-in', function() {
      assert.ok(true, "sign in modal was displayed");
      done();
    });
  });
});

describe("GuestNav", function() {
  beforeEach(function() {
    testUtils.initEmptyStore(store);
    testUtils.initDropdown(dropdown);
    testUtils.initModal(modal);

    misago._context = {
      'FORGOTTEN_PASSWORD_URL': '/forgotten-password/'
    };

    /* jshint ignore:start */
    testUtils.render(<GuestNav />);
    /* jshint ignore:end */
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders', function() {
    let element = $('#test-mount .nav-guest');
    assert.ok(element.length, "component renders");
  });

  it('opens sign in modal on click', function(done) {
    testUtils.simulateClick('#test-mount .btn-default');

    testUtils.onElement('#modal-mount .modal-sign-in', function() {
      assert.ok(true, "sign in modal was displayed");
      done();
    });
  });
});

describe("CompactGuestNav", function() {
  beforeEach(function() {
    testUtils.initEmptyStore(store);
    testUtils.initDropdown(dropdown);

    /* jshint ignore:start */
    testUtils.render(<CompactGuestNav />);
    /* jshint ignore:end */
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders', function() {
    let element = $('#test-mount img.user-avatar');
    assert.ok(element.length, "component renders");
  });

  it('opens dropdown on click', function() {
    testUtils.simulateClick('#test-mount button');

    let element = $('#dropdown-mount>.dropdown-menu');
    assert.ok(element.length, "component opened dropdown");
  });
});
