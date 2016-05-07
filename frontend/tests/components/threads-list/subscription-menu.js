import assert from 'assert';
import React from 'react'; // jshint ignore:line
import SubscriptionMenu from 'misago/components/threads-list/thread/subscription/options'; // jshint ignore:line
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';
import Store from 'misago/services/store';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
const thread = {
  id: 123,
  api_url: '/test-api/threads/1321/',
  subscription: null
};

describe("Threads List Subscription Options", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);
    testUtils.initModal(modal);
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("handles backend error", function(done) {
    Store._store = {
      dispatch: function(action) {
        this.action = action;
      }
    };

    $.mockjax({
      url: thread.api_url,
      status: 500
    });

    /* jshint ignore:start */
    testUtils.render(<SubscriptionMenu thread={thread} />);
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount button:eq(2)');

    window.setTimeout(function() {
      assert.deepEqual(Store._store.action, {
        type: 'PATCH_THREAD',
        thread: {
          id: 123,
          api_url: '/test-api/threads/1321/',
          subscription: null
        },
        patch: {
          subscription: null
        },
        sorting: null
      }, "action was set on store");

      assert.deepEqual(snackbarStore.message, {
        message: 'Unknown error has occured.',
        type: 'error'
      });

      done();
    }, 300);
  });

  it("unsubscribes thread", function(done) {
    Store._store = {
      dispatch: function(action) {
        this.action = action;
      }
    };

    $.mockjax({
      url: thread.api_url,
      status: 200,
      responseText: {
        subscription: null
      }
    });

    /* jshint ignore:start */
    testUtils.render(<SubscriptionMenu thread={thread} />);
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount button:eq(0)');

    window.setTimeout(function() {
      assert.deepEqual(Store._store.action, {
        type: 'PATCH_THREAD',
        thread: {
          id: 123,
          api_url: '/test-api/threads/1321/',
          subscription: null
        },
        patch: {
          subscription: null
        },
        sorting: null
      }, "action was set on store");

      done();
    }, 300);
  });

  it("subscribes thread", function(done) {
    Store._store = {
      dispatch: function(action) {
        this.action = action;
      }
    };

    $.mockjax({
      url: thread.api_url,
      status: 200,
      responseText: {
        subscription: false
      }
    });

    /* jshint ignore:start */
    testUtils.render(<SubscriptionMenu thread={thread} />);
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount button:eq(1)');

    window.setTimeout(function() {
      assert.deepEqual(Store._store.action, {
        type: 'PATCH_THREAD',
        thread: {
          id: 123,
          api_url: '/test-api/threads/1321/',
          subscription: null
        },
        patch: {
          subscription: false
        },
        sorting: null
      }, "action was set on store");

      done();
    }, 300);
  });

  it("subscribes thread with email", function(done) {
    Store._store = {
      dispatch: function(action) {
        this.action = action;
      }
    };

    $.mockjax({
      url: thread.api_url,
      status: 200,
      responseText: {
        subscription: true
      }
    });

    /* jshint ignore:start */
    testUtils.render(<SubscriptionMenu thread={thread} />);
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount button:eq(2)');

    window.setTimeout(function() {
      assert.deepEqual(Store._store.action, {
        type: 'PATCH_THREAD',
        thread: {
          id: 123,
          api_url: '/test-api/threads/1321/',
          subscription: null
        },
        patch: {
          subscription: true
        },
        sorting: null
      }, "action was set on store");

      done();
    }, 300);
  });
});