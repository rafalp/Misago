import moment from 'moment';
import assert from 'assert';
import reducer, { updateAvatar, hydrate, hydrateStatus } from 'misago/reducers/users';

describe("Users Reducer", function() {
  it("hydrates result", function() {
    let timestamp = moment().format();
    let state = reducer([], hydrate([
      {
        something: 'ok',
        status: null
      },
      {
        something: 'okie',
        status: {
          last_click: timestamp,
          banned_until: timestamp
        }
      },
    ]));

    assert.equal(state[0].status, null, "reducer left empty status unchanged");
    assert.equal(state[0].something, 'ok', "other keys were unconverted");

    assert.equal(state[1].status.last_click.format(), timestamp,
      "reducer deserialized user's status");
    assert.equal(state[1].something, 'okie', "other keys were unconverted");
  });

  it("updates avatar", function() {
    let state = [
      {
        id: 123,
        status: null,
        avatar_hash: 'aabbccdd'
      }
    ];

    assert.deepEqual(reducer(state, updateAvatar({
      id: 123
    }, '11223344')), [
      {
        id: 123,
        status: null,
        avatar_hash: '11223344'
      }
    ], "reducer updates user avatar");

    assert.deepEqual(reducer(state, updateAvatar({
      id: 321
    }, '11223344')), [
      {
        id: 123,
        status: null,
        avatar_hash: 'aabbccdd'
      }
    ], "reducer validates user id");
  });
});

describe("hydrate User Status", function() {
  it("hydrates status", function() {
    let timestamp = moment().format();
    let status = hydrateStatus({
      some_key: true,
      last_click: timestamp,
      banned_until: null
    });

    assert.equal(status.some_key, true, "non-special key was preserved");
    assert.equal(status.last_click.format(), timestamp,
      "last click key was hydrated");
    assert.equal(status.banned_until, null, "ban date was hydrated");

    assert.equal(hydrateStatus(null), null, "null state was handled");
  });
});