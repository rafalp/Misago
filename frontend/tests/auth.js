import assert from 'assert';
import { updateAvatar, updateUsername } from 'misago/reducers/users';
import reducer, { SIGN_IN, SIGN_OUT, signIn, signOut, patchUser } from 'misago/reducers/auth';
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

describe("Auth Reducer", function() {
  it("patches auth user", function() {
    let state = {
      user: {
        username: 'Original'
      }
    };

    assert.deepEqual(reducer(state, patchUser({
      username: 'Patched!',
      new_attr: 'Set'
    })), {
      user: {
        username: 'Patched!',
        new_attr: 'Set'
      }
    }, "reducer patched authenticated user");
  });

  it("updates avatar", function() {
    let state = {
      isAuthenticated: true,
      user: {
        id: 321,
        avatar_hash: 'aabbccdd'
      }
    };

    assert.deepEqual(reducer(state, updateAvatar({
      id: 321
    }, '11223344')), {
      isAuthenticated: true,
      user: {
        id: 321,
        avatar_hash: '11223344'
      }
    }, "reducer changed authenticated user's avatar hash");

    assert.deepEqual(reducer(state, updateAvatar({
      id: 322
    }, '11223344')), {
      isAuthenticated: true,
      user: {
        id: 321,
        avatar_hash: 'aabbccdd'
      }
    }, "reducer validates user id");
  });

  it("updates username", function() {
    let state = {
      isAuthenticated: true,
      user: {
        id: 321,
        username: 'Bob',
        slug: 'bob'
      }
    };

    assert.deepEqual(reducer(state, updateUsername({
      id: 321
    }, 'Weebl', 'weebl')), {
      isAuthenticated: true,
      user: {
        id: 321,
        username: 'Weebl',
        slug: 'weebl'
      }
    }, "reducer changed authenticated user's name");

    assert.deepEqual(reducer(state, updateUsername({
      id: 322
    }, 'Weebl', 'weebl')), {
      isAuthenticated: true,
      user: {
        id: 321,
        username: 'Bob',
        slug: 'bob'
      }
    }, "reducer validates user id");
  });

  it("signs user in", function() {
    let state = {
      signedIn: false
    };

    assert.deepEqual(reducer(state, signIn({username: 'Weebl'})), {
      signedIn: {
        username: 'Weebl'
      }
    }, "reducer changed store state for sign in");
  });

  it("signs user out", function() {
    let state = {
      isAuthenticated: true,
      isAnonymous: true,
      signedIn: false,
      signedOut: true
    };

    assert.deepEqual(reducer(state, signOut()), {
      isAuthenticated: false,
      isAnonymous: true,
      signedIn: false,
      signedOut: true
    }, "reducer changed store state for sign out");
  });

  it("soflty signs user out", function() {
    let state = {
      isAuthenticated: true,
      isAnonymous: true,
      signedIn: false,
      signedOut: true
    };

    assert.deepEqual(reducer(state, signOut(true)), {
      isAuthenticated: false,
      isAnonymous: true,
      signedIn: false,
      signedOut: false
    }, "reducer changed store state for soft sign out");
  });
});