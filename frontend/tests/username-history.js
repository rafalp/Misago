import moment from 'moment';
import assert from 'assert';
import { updateAvatar, updateUsername } from 'misago/reducers/users';
import reducer, { addNameChange, hydrate, append } from 'misago/reducers/username-history';

describe("Username History Reducer", function() {
  it("hydrates result", function() {
    let timestamp = moment().format();
    let state = reducer([], hydrate([
      {
        something: 'ok',
        changed_on: timestamp
      }
    ]));

    assert.equal(state[0].changed_on.format(), timestamp,
      "reducer converted changed_on timestamp to moment.js object");
    assert.equal(state[0].something, 'ok', "other keys were unconverted");
  });

  it("appends result", function() {
    let timestamp = moment().format();
    let state = reducer([
      {
        order: 'first',
        changed_on: timestamp
      }
    ], append([
      {
        order: 'second',
        changed_on: timestamp
      }
    ]));

    assert.equal(state[0].order, 'first', "original item was kept");
    assert.equal(state[1].order, 'second', "new item was appended");
  });

  it("prepends namechange", function() {
    let user = {
      username: 'Bob'
    };

    let changedBy = {
      id: 123,
      username: 'Weebl',
    };

    let state = reducer([{
      something: 'ok'
    }], addNameChange({username: 'Nopp'}, user, changedBy));

    assert.equal(state[0].new_username, 'Nopp',
      "reducer inserted new username to store");
    assert.equal(state[0].old_username, 'Bob',
      "reducer inserted old username to store");
    assert.equal(state[0].changed_by, changedBy,
      "reducer preserved change author");
    assert.equal(state[0].changed_by_username, 'Weebl',
      "reducer preserved username from change author");
    assert.equal(state[1].something, 'ok', "old entries were pushed down");
  });

  it("updates avatar", function() {
    let state = [
      {
        changed_by: {
          id: 123,
          avatar_hash: 'aabbccdd'
        }
      }
    ];

    assert.deepEqual(reducer(state, updateAvatar({
      id: 123
    }, '11223344')), [
      {
        changed_by: {
          id: 123,
          avatar_hash: '11223344'
        }
      }
    ], "reducer updates change author avatar");

    assert.deepEqual(reducer(state, updateAvatar({
      id: 321
    }, '11223344')), [
      {
        changed_by: {
          id: 123,
          avatar_hash: 'aabbccdd'
        }
      }
    ], "reducer validates change author id");
  });

  it("updates username", function() {
    let state = [
      {
        changed_by: {
          id: 123,
          username: 'Bob',
          slug: 'bob'
        }
      }
    ];

    assert.deepEqual(reducer(state, updateUsername({
      id: 123
    }, 'Weebl', 'weebl')), [
      {
        changed_by: {
          id: 123,
          username: 'Weebl',
          slug: 'weebl'
        }
      }
    ], "reducer updates change author username");

    assert.deepEqual(reducer(state, updateUsername({
      id: 321
    }, 'Weebl', 'weebl')), [
      {
        changed_by: {
          id: 123,
          username: 'Bob',
          slug: 'bob'
        }
      }
    ], "reducer validates change author id");
  });
});