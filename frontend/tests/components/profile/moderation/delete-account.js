import assert from 'assert';
import React from 'react'; // jshint ignore:line
import DeleteAccount from 'misago/components/profile/moderation/delete-account'; // jshint ignore:line
import polls from 'misago/services/polls';
import snackbar from 'misago/services/snackbar';
import * as testUtils from 'misago/utils/test-utils';

let component = null;
let snackbarStore = null;
let profileMock = {
  id: 242,
  avatar_hash: 'original_hash',
  username: "BobBoberson",

  is_followed: false,
  followers: 0,

  api_url: {
    delete: '/test-api/users/123/delete/'
  }
};

describe("User Profile Deletion", function() {
  beforeEach(function() {
    component = null;

    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    polls.init();
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function(done) {
    $.mockjax({
      url: profileMock.api_url.delete,
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    /* jshint ignore:start */
    component = testUtils.render(<DeleteAccount profile={profileMock} />)
    /* jshint ignore:end */

    testUtils.onElement('#test-mount form', function(element) {
      assert.ok(element.length, "component loads");

      let btn = element.find('.btn-danger');
      assert.equal(btn.text().indexOf("Please wait..."), 0,
        "countdown is displayed in button");

      component.setState({
        countdown: 0,
        confirm: true
      });

      component.forceUpdate(function() {
        assert.equal(btn.text(), "Delete BobBoberson", "countdown ends");

        done();
      });
    });
  });

  it("handles backend error", function(done) {
    $.mockjax({
      url: profileMock.api_url.delete,
      status: 500
    });

    /* jshint ignore:start */
    testUtils.render(<DeleteAccount profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-message', function(element) {
      assert.equal(element.find('p.lead').text(), "Unknown error has occured.",
        "error message renders");

      done();
    });
  });

  it("handles load rejection", function(done) {
    $.mockjax({
      url: profileMock.api_url.delete,
      status: 403,
      responseText: {
        detail: "You can't nuke user!"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<DeleteAccount profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-message', function(element) {
      assert.equal(element.find('p.lead').text(), "You can't nuke user!",
        "error message renders");

      done();
    });
  });

  it("handles failed submission", function(done) {
    $.mockjax({
      url: profileMock.api_url.delete,
      type: 'GET',
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    $.mockjax({
      url: profileMock.api_url.delete,
      type: 'POST',
      status: 400,
      responseText: {
        detail: "Can't do it now!"
      }
    });

    /* jshint ignore:start */
    component = testUtils.render(<DeleteAccount profile={profileMock} />)
    /* jshint ignore:end */

    snackbarStore.callback(function(message) {
      assert.equal(message.message, "Can't do it now!",
        "Rejection message is shown in snackbar.");

      done();
    });

    testUtils.onElement('#test-mount form', function() {
      component.setState({
        countdown: 0,
        confirm: true
      });

      component.forceUpdate(function() {
        testUtils.simulateSubmit('#test-mount form');
      });
    });
  });

  it("delets account without content", function(done) {
    $.mockjax({
      url: profileMock.api_url.delete,
      type: 'GET',
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    $.mockjax({
      url: profileMock.api_url.delete,
      type: 'POST',
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    /* jshint ignore:start */
    component = testUtils.render(<DeleteAccount profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount form', function() {
      component.setState({
        countdown: 0,
        confirm: true
      });

      component.forceUpdate(function() {
        testUtils.simulateSubmit('#test-mount form');
      });

      testUtils.onElement('#test-mount .modal-message', function(element) {
        assert.equal(element.find('p.lead').text(),
          "BobBoberson's account has been deleted and other content has been hidden.",
          "valid account deletion message was displayed");

        done();
      });
    });
  });

  it("delets account with content", function(done) {
    $.mockjax({
      url: profileMock.api_url.delete,
      type: 'GET',
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    $.mockjax({
      url: profileMock.api_url.delete,
      type: 'POST',
      status: 200,
      responseText: {
        detail: 'ok'
      }
    });

    /* jshint ignore:start */
    component = testUtils.render(<DeleteAccount profile={profileMock} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount form', function() {
      component.setState({
        countdown: 0,
        confirm: true,
        with_content: true
      });

      component.forceUpdate(function() {
        testUtils.simulateSubmit('#test-mount form');
      });

      testUtils.onElement('#test-mount .modal-message', function(element) {
        assert.equal(element.find('p.lead').text(),
          "BobBoberson's account, threads, posts and other content has been deleted.",
          "valid account deletion message was displayed");

        done();
      });
    });
  });
});