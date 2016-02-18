import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Nav from 'misago/components/profile/moderation/nav'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

let profileMock = null;

describe("User Profile Moderation Menu", function() {
  beforeEach(function() {
    profileMock = {
      acl: {
        can_moderate_avatar: false,
        can_rename: false,
        can_delete: false
      }
    };
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    testUtils.render(<Nav profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .dropdown-menu');
    assert.ok(element.length, "component renders");

    assert.ok(!element.find('.btn-link').length,
      "no moderation buttons are defautly displayed");
  });

  it("renders avatar moderation button", function() {
    /* jshint ignore:start */
    profileMock.acl.can_moderate_avatar = true;
    testUtils.render(<Nav profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .dropdown-menu');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('.btn-link').length, 1,
      "moderation button is displayed");

    assert.equal(element.find('.btn-link .material-icon').text(), 'portrait',
      "avatar moderation button has valid icon");
    assert.ok(element.find('.btn-link').text().indexOf("Avatar controls") > 0,
      "avatar moderation button has valid label");
  });

  it("renders username moderation button", function() {
    /* jshint ignore:start */
    profileMock.acl.can_rename = true;
    testUtils.render(<Nav profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .dropdown-menu');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('.btn-link').length, 1,
      "moderation button is displayed");

    assert.equal(element.find('.btn-link .material-icon').text(), 'credit_card',
      "username moderation button has valid icon");
    assert.ok(element.find('.btn-link').text().indexOf("Change username") > 0,
      "username moderation button has valid label");
  });

  it("renders delete button", function() {
    /* jshint ignore:start */
    profileMock.acl.can_delete = true;
    testUtils.render(<Nav profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .dropdown-menu');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('.btn-link').length, 1,
      "moderation button is displayed");

    assert.equal(element.find('.btn-link .material-icon').text(), 'clear',
      "delete user button has valid icon");
    assert.ok(element.find('.btn-link').text().indexOf("Delete account") > 0,
      "delete user button has valid label");
  });

  it("renders menu toggle", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    let toggleNav = function() {
      assert.ok(true, "callback was called!");
      done();
    }
    testUtils.render(<Nav profile={profileMock} toggleNav={toggleNav} />);
    /* jshint ignore:end */

    let element = $('#test-mount .dropdown-menu');
    assert.ok(element.length, "component renders");

    testUtils.simulateClick('.btn-default');
  });
});