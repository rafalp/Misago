import assert from 'assert';
import { SIGN_IN, SIGN_OUT } from 'misago/reducers/auth';
import { Auth } from 'misago/services/auth';

let auth = null;

describe("Auth", function() {
  it("synces authenticated session", function(done) {
    let store = {
      getState: function() {
        return {
          auth: {
            isAuthenticated: true,
            user: {
              username: 'BobBoberson'
            }
          }
        };
      }
    };

    let local = {
      set: function(name, value) {
        assert.equal(name, 'auth', "synced session key is valid");
        assert.deepEqual(value, {
          isAuthenticated: true,
          username: 'BobBoberson'
        }, "new session state is valid");
        done();
      },
      watch: function() {
        /* noop */
      }
    };

    let modal = {
      hide: function() {
        /* noop */
      }
    };

    auth = new Auth();
    auth.init(store, local, modal);
  });

  it("synces anonymous session", function(done) {
    let store = {
      getState: function() {
        return {
          auth: {
            isAuthenticated: false
          }
        };
      }
    };

    let local = {
      set: function(name, value) {
        assert.equal(name, 'auth', "synced session key is valid");
        assert.deepEqual(value, {
          isAuthenticated: false
        }, "new session state is valid");
        done();
      },
      watch: function() {
        /* noop */
      }
    };

    let modal = {
      hide: function() {
        /* noop */
      }
    };

    auth = new Auth();
    auth.init(store, local, modal);
  });

  it("watches session sign in", function(done) {
    let store = {
      getState: function() {
        return {
          auth: {
            isAuthenticated: false
          }
        };
      },
      dispatch(action) {
        assert.deepEqual(action, {
          type: SIGN_IN,
          user: {
            username: 'BobBoberson'
          }
        }, "action was dispatched");
        done();
      }
    };

    let local = {
      set: function() {
        /* noop */
      },
      watch: function(name, callable) {
        assert.equal(name, 'auth', "watched session key is valid");
        assert.ok(callable, "callback is provided");

        callable({
          isAuthenticated: true,
          username: 'BobBoberson'
        });
      }
    };

    let modal = {
      hide: function() {
        /* noop */
      }
    };

    auth = new Auth();
    auth.init(store, local, modal);
  });

  it("watches session sign out", function(done) {
    let store = {
      getState: function() {
        return {
          auth: {
            isAuthenticated: false
          }
        };
      },
      dispatch(action) {
        assert.deepEqual(action, {
          type: SIGN_OUT,
          soft: false
        }, "action was dispatched");
        done();
      }
    };

    let local = {
      set: function() {
        /* noop */
      },
      watch: function(name, callable) {
        assert.equal(name, 'auth', "watched session key is valid");
        assert.ok(callable, "callback is provided");

        callable({
          isAuthenticated: false
        });
      }
    };

    let modal = {
      hide: function() {
        assert.ok(true, 'modal was hidden');
      }
    };

    auth = new Auth();
    auth.init(store, local, modal);
  });
});