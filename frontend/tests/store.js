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

  it("initializes and returns state", function() {
    function testReducer(state={}, action=null) { // jshint ignore:line
      if (state.initial == 'state') {
        assert.ok("reducer was called on initializaiton");
        return {'initial': 'reduced'};
      } else {
        return state;
      }
    }

    store = new StoreWrapper();
    store.addReducer('test', testReducer, {'initial': 'state'});
    store.init();

    assert.deepEqual(store.getState().test, {'initial': 'reduced'},
      "state was changed by test reducer");
  });

  it("dispatches actions", function() {
    function testReducer(state={}, action=null) {
      if (action.type == 'test') {
        assert.ok("reducer was called on action");
        return {'state': action.new_state};
      } else {
        return state;
      }
    }

    store = new StoreWrapper();
    store.addReducer('test', testReducer, {'state': 'initial'});
    store.init();

    store.dispatch({'type': 'test', 'new_state': 'changed'});

    assert.deepEqual(store.getState().test, {'state': 'changed'},
      "state was changed by test reducer");
  });
});
