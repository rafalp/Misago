import assert from 'assert';
import moment from 'moment';
import React from 'react'; // jshint ignore:line
import BanDetails from 'misago/components/profile/ban-details'; // jshint ignore:line
import misago from 'misago/index';
import ajax from 'misago/services/ajax';
import polls from 'misago/services/polls';
import * as testUtils from 'misago/utils/test-utils';

let profileMock = {
  username: 'BobBoberson',

  api_url: {
    ban: '/test-api/users/123/just-ban/'
  }
};
let expires_on = moment().add(5, 'days');

describe("User Profile Ban Details", function() {
  beforeEach(function() {
    polls.init(ajax, null);
  });

  afterEach(function() {
    testUtils.unmountComponents();
    $.mockjax.clear();
    polls.stop('ban-details');
  });

  it("preloads", function(done) {
    misago._context.PROFILE_BAN = {
      user_message: null,
      staff_message: null,
      expires_on: null
    };

    $.mockjax({
      url: profileMock.api_url.ban,
      status: 200,
      responseText: {
        user_message: null,
        staff_message: null,
        expires_on: null
      }
    });

    /* jshint ignore:start */
    testUtils.render(<BanDetails profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .ban-expires p.lead', function(element) {
      assert.equal(element.text(), "BobBoberson's ban is permanent.",
        "expiration message is displayed");

      assert.ok(!$('#test-mount .ban-user-message').length,
        "user message is hidden");
      assert.ok(!$('#test-mount .ban-staff-message').length,
        "staff message is hidden");

      done();
    });
  });

  it("loads", function(done) {
    $.mockjax({
      url: profileMock.api_url.ban,
      status: 200,
      responseText: {
        user_message: null,
        staff_message: null,
        expires_on: null
      }
    });

    /* jshint ignore:start */
    testUtils.render(<BanDetails profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .ban-expires p.lead', function(element) {
      assert.equal(element.text(), "BobBoberson's ban is permanent.",
        "expiration message is displayed");

      assert.ok(!$('#test-mount .ban-user-message').length,
        "user message is hidden");
      assert.ok(!$('#test-mount .ban-staff-message').length,
        "staff message is hidden");

      done();
    });
  });

  it("loads kitchensink", function(done) {
    $.mockjax({
      url: profileMock.api_url.ban,
      status: 200,
      responseText: {
        user_message: {
          plain: "Test user message.",
          html: "<p>Test user message.</p>"
        },
        staff_message: {
          plain: "Test staff message.",
          html: "<p>Test staff message.</p>"
        },
        expires_on: expires_on.format()
      }
    });

    /* jshint ignore:start */
    testUtils.render(<BanDetails profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .ban-expires p.lead', function(element) {
      assert.equal(element.text(), "This ban expires in 5 days.",
        "expiration message is displayed");

      assert.equal($('#test-mount .ban-user-message p').text(),
        "Test user message.",
        "user message is displayed");

      assert.equal($('#test-mount .ban-staff-message p').text(),
        "Test staff message.",
        "staff message is displayed");

      done();
    });
  });

  it("loads no ban", function(done) {
    $.mockjax({
      url: profileMock.api_url.ban,
      status: 200,
      responseText: {}
    });

    /* jshint ignore:start */
    testUtils.render(<BanDetails profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .panel-message-body', function(element) {
      assert.equal(element.find('p').text(), "No ban is active at the moment.",
        "no ban message is displayed");

      done();
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: profileMock.api_url.ban,
      status: 500
    });

    /* jshint ignore:start */
    testUtils.render(<BanDetails profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .panel-message-body', function(element) {
      assert.equal(element.find('p').text(), "Unknown error has occured.",
        "rejection message is displayed");

      done();
    });
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: profileMock.api_url.ban,
      status: 403,
      responseText: {
        detail: "You can't into user bans!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<BanDetails profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .panel-message-body', function(element) {
      assert.equal(element.find('p').text(), "You can't into user bans!",
        "rejection message is displayed");

      done();
    });
  });
});