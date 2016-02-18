import assert from 'assert';
import moment from 'moment';
import React from 'react'; // jshint ignore:line
import Header from 'misago/components/profile/header'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

let profileMock = null;

describe("User Profile Header", function() {
  beforeEach(function() {
    profileMock = {
      id: 42,
      username: "BobBoberson",
      email: '',

      joined_on: moment(),

      title: '',
      rank: {
        id: 321,
        name: "Test Rank",
        slug: "test-rank",
        css_class: '',
        is_tab: false,
        title: ''
      },

      status: {
        is_online: true
      },

      is_followed: false,

      acl: {
        can_follow: false,
        can_moderate: false
      }
    };
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    testUtils.render(<Header profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('h1 .user-name').text(), profileMock.username,
      "header displays correct username");

    assert.equal(element.find('.user-joined-on abbr').text(),
      "Joined a few seconds ago",
      "correct join date is displayed");

    assert.equal(element.find('.user-rank span').text(), "Test Rank",
      "correct rank name is displaued");

    assert.ok(element.find('.user-status-display').length,
      "user status is displayed");

    assert.ok(!element.find('.user-title').length, "no title is displayed");
    assert.ok(!element.find('.user-email').length, "no email is displayed");

    assert.ok(!element.find('.btn-follow').length,
      "follow button is hidden");
    assert.ok(!element.find('.btn-moderate').length,
      "moderate button is hidden");
  });

  it("renders follow button", function() {
    /* jshint ignore:start */
    profileMock.acl.can_follow = true;
    testUtils.render(<Header profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header');
    assert.ok(element.length, "component renders");

    assert.ok(element.find('.btn-follow').length,
      "follow button is shown");
  });

  it("renders moderation button", function() {
    /* jshint ignore:start */
    profileMock.acl.can_moderate = true;
    testUtils.render(<Header profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header');
    assert.ok(element.length, "component renders");

    assert.ok(element.find('.btn-moderate').length,
      "moderate button is shown");
  });

  it("renders email", function() {
    /* jshint ignore:start */
    profileMock.email = 'lorem@ipsum.com';
    testUtils.render(<Header profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header');
    assert.ok(element.length, "component renders");

    assert.ok(element.find('.user-email a').text(), 'lorem@ipsum.com',
      "email address renders");
  });

  it("renders user title", function() {
    /* jshint ignore:start */
    profileMock.title = "Test User";
    testUtils.render(<Header profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header');
    assert.ok(element.length, "component renders");

    assert.ok(element.find('.user-title').text(), "Test User",
      "user title renders");
  });

  it("renders rank title", function() {
    /* jshint ignore:start */
    profileMock.rank.title = "Test Rank User";
    testUtils.render(<Header profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header');
    assert.ok(element.length, "component renders");

    assert.ok(element.find('.user-title').text(), "Test Rank User",
      "user rank title renders");
  });

  it("renders rank url", function() {
    /* jshint ignore:start */
    profileMock.rank.is_tab = true;
    profileMock.rank.absolute_url = '/rank-url/';
    testUtils.render(<Header profile={profileMock} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header');
    assert.ok(element.length, "component renders");

    assert.ok(element.find('.user-rank a').text(), profileMock.rank.name,
      "user rank renders as link to profile");
  });

  it("renders compact menu toggle", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    let toggleNav = function() {
      assert.ok(true, "callback was called!");
      done();
    }
    testUtils.render(<Header profile={profileMock} toggleNav={toggleNav} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header');
    assert.ok(element.length, "component renders");

    testUtils.simulateClick('.btn-dropdown-toggle');
  });
});