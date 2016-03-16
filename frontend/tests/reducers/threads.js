import assert from 'assert';
import moment from 'moment';
import reducer, { append, hydrate, hydrateThread } from 'misago/reducers/threads';

describe("Threads Reducer", function() {
  it("hydrates thread", function() {
    let timestamp = moment().format();
    let thread = hydrateThread({
      started_on: timestamp,
      last_post_on: timestamp
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
        last_post_on: timestamp
      },
      {
        id: 3,
        started_on: timestamp,
        last_post_on: timestamp
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
        last_post: 4
      },
      {
        id: 3,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 1
      }
    ], append([
      {
        id: 1,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 5
      },
      {
        id: 2,
        started_on: timestamp,
        last_post_on: timestamp,
        last_post: 3
      }
    ]));

    assert.equal(threads.length, 3, "one thread was added to state");

    assert.equal(threads[0].id, 1, "first thread wasn't moved");
    assert.equal(threads[0].last_post, 5, "first thread was updated");
    assert.equal(threads[1].id, 2, "new thread was appended as second");
    assert.equal(threads[2].id, 3, "old second thread is now last");
  });
});