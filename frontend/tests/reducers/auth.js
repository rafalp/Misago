import assert from 'assert';
import { updateAvatar, updateUsername } from 'misago/reducers/users';
import reducer, { signIn, signOut, patch } from 'misago/reducers/auth';

describe("Auth Reducer", function() {
  it("patches auth user", function() {
    let state = {
      user: {
        username: 'Original'
      }
    };

    assert.deepEqual(reducer(state, patch({
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