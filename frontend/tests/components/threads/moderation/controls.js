import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Controls from 'misago/components/threads/moderation/controls'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Threads List Moderation Controls Display", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });
});

describe("Threads List Moderation Controls Display", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("shows no buttons", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Controls className="test-controls" moderation={{
        can_approve: false,
        can_close: false,
        can_hide: false,
        can_move: false,
        can_merge: false,
        can_pin: false
      }} />
    );
    /* jshint ignore:end */

    const element = $('#test-mount .test-controls');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('li').length, 0,
      "moderation controls are hidden");
  });

  it("shows pin/unpin buttons", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Controls className="test-controls" moderation={{
        can_approve: false,
        can_close: false,
        can_hide: false,
        can_move: false,
        can_merge: false,
        can_pin: 1
      }} />
    );
    /* jshint ignore:end */

    const element = $('#test-mount .test-controls');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('li').length, 2,
      "pin/unpin moderation controls are shown");
  });

  it("shows pin locally/globally/unpin buttons", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Controls className="test-controls" moderation={{
        can_approve: false,
        can_close: false,
        can_hide: false,
        can_move: false,
        can_merge: false,
        can_pin: 2
      }} />
    );
    /* jshint ignore:end */

    const element = $('#test-mount .test-controls');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('li').length, 3,
      "pin locally/globally/unpin moderation controls are shown");
  });

  it("shows move button", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Controls className="test-controls" moderation={{
        can_approve: false,
        can_close: false,
        can_hide: false,
        can_move: true,
        can_merge: false,
        can_pin: false
      }} />
    );
    /* jshint ignore:end */

    const element = $('#test-mount .test-controls');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('li').length, 1,
      "move moderation controls are shown");
  });

  it("shows merge button", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Controls className="test-controls" moderation={{
        can_approve: false,
        can_close: false,
        can_hide: false,
        can_move: false,
        can_merge: true,
        can_pin: false
      }} />
    );
    /* jshint ignore:end */

    const element = $('#test-mount .test-controls');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('li').length, 1,
      "merge moderation controls are shown");
  });

  it("shows approve button", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Controls className="test-controls" moderation={{
        can_approve: true,
        can_close: false,
        can_hide: false,
        can_move: false,
        can_merge: false,
        can_pin: false
      }} />
    );
    /* jshint ignore:end */

    const element = $('#test-mount .test-controls');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('li').length, 1,
      "approve moderation controls are shown");
  });

  it("shows close/open buttons", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Controls className="test-controls" moderation={{
        can_approve: false,
        can_close: true,
        can_hide: false,
        can_move: false,
        can_merge: false,
        can_pin: false
      }} />
    );
    /* jshint ignore:end */

    const element = $('#test-mount .test-controls');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('li').length, 2,
      "close/open moderation controls are shown");
  });

  it("shows hide/unhide buttons", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Controls className="test-controls" moderation={{
        can_approve: false,
        can_close: false,
        can_hide: true,
        can_move: false,
        can_merge: false,
        can_pin: false
      }} />
    );
    /* jshint ignore:end */

    const element = $('#test-mount .test-controls');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('li').length, 2,
      "hide/unhide moderation controls are shown");
  });

  it("shows hide/delete/unhide buttons", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Controls className="test-controls" moderation={{
        can_approve: false,
        can_close: false,
        can_hide: 2,
        can_move: false,
        can_merge: false,
        can_pin: false
      }} />
    );
    /* jshint ignore:end */

    const element = $('#test-mount .test-controls');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('li').length, 3,
      "hide/delete/unhide moderation controls are shown");
  });
});