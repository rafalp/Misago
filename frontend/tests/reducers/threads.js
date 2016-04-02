import assert from 'assert';
import moment from 'moment';
import reducer, { append, hydrate, patch, read, hydrateThread } from 'misago/reducers/threads';

describe("Threads Reducer", function() {
  it("hydrates thread", function() {
    let timestamp = moment().format();
    let thread = hydrateThread({
      started_on: timestamp,
      last_post_on: timestamp,
      acl: {}
    });

    assert.equal(thread.started_on.format(), timestamp,
      "thread start date was hydrated");
    assert.equal(thread.last_post_on.format(), timestamp,
      "thread last reply date was hydrated");
  });

  it("hydrates threads list", function() {
    let timestamp = moment().format();
    let threads = reducer([], hydrate([
      {
        id: 1,
        started_on: timestamp,
        last_post_on: timestamp,
        acl: {}
      },
      {
        id: 3,
        started_on: timestamp,
        last_post_on: timestamp,
        acl: {}
      }
    ]));

    assert.equal(threads.length, 2,
      "two threads were hydrated and set as state");

    assert.equal(threads[0].started_on.format(), timestamp,
      "first thread was hydrated");
    assert.equal(threads[1].started_on.format(), timestamp,
      "second thread was hydrated");
  });

  it("appends threads to list", function() {
    let timestamp = moment().format();
    let threads = reducer([
      {
        id: 1,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 4,
        acl: {}
      },
      {
        id: 3,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 1,
        acl: {}
      }
    ], append([
      {
        id: 1,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 5,
        acl: {}
      },
      {
        id: 2,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 3,
        acl: {}
      }
    ]));

    assert.equal(threads.length, 3, "one thread was added to state");

    assert.equal(threads[0].id, 1, "first thread wasn't moved");
    assert.equal(threads[0].last_post, 5, "first thread was updated");
    assert.equal(threads[1].id, 2, "new thread was appended as second");
    assert.equal(threads[2].id, 3, "old second thread is now last");
  });

  it("patches thread", function() {
    let timestamp = moment().format();
    let threads = reducer([
      {
        id: 1,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 4
      },
      {
        id: 3,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 1
      }
    ], patch({id: 3}, {
      id: 3,
      patch: 'yep'
    }));

    assert.equal(threads.length, 2, "state length remained same");

    assert.equal(threads[0].patch, undefined, "first thread wasn't changed");
    assert.equal(threads[1].patch, 'yep', "second thread was patched");
  });

  it("marks threads as read", function() {
    let timestamp = moment().format();
    let threads = reducer([
      {
        id: 1,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 4,
        is_read: false
      },
      {
        id: 3,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 1,
        is_read: false
      }
    ], read());

    assert.equal(threads.length, 2, "state length remained same");

    assert.ok(threads[0].is_read, "first thread was marked as read");
    assert.ok(threads[1].is_read, "second thread was marked as read");
  });
});