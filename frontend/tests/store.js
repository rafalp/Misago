import assert from 'assert';
import { StoreWrapper } from 'misago/services/store';

var store = null;

describe('Store', function() {
  it("addReducer registers new reducer", function() {
    store = new StoreWrapper();

    store.addReducer('test', 'reducer', {'initial': 'state'});

    assert.equal(store._reducers.test, 'reducer',
      "test reducer was registered");
    assert.deepEqual(store._initialState.test, {'initial': 'state'},
      "test reducer initial state was registered");
  });
});
