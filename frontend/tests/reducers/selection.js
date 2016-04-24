import assert from 'assert';
import { StoreWrapper } from 'misago/services/store';
import reducer, { all, none, item } from 'misago/reducers/selection';

let store = null;

describe("Selection", function() {
  beforeEach(function() {
    store = new StoreWrapper();
    store.addReducer('selection', reducer, []);
    store.init();
  });

  it("all", function() {
    store.dispatch(all([1, 2, 3]));
    assert.deepEqual(store.getState().selection, [1, 2, 3],
      "all() replaces state with new one");
  });

  it("none", function() {
    store.dispatch(all([1, 2, 3]));
    store.dispatch(none());

    assert.deepEqual(store.getState().selection, [],
      "none() replaces state with empty one");
  });

  it("item", function() {
    store.dispatch(item(2));
    assert.deepEqual(store.getState().selection, [2],
      "item(2) toggles item in");

    store.dispatch(item(2));
    assert.deepEqual(store.getState().selection, [],
      "item(2) toggles item out");
  });
});