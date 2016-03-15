import assert from 'assert';
import { StoreWrapper } from 'misago/services/store';
import reducer, { initialState, showSnackbar, hideSnackbar } from 'misago/reducers/snackbar';

let store = null;

describe("Snackbar", function() {
  beforeEach(function() {
    store = new StoreWrapper();
    store.addReducer('snackbar', reducer, initialState);
    store.init();
  });

  it("showSnackbar action sets new message", function() {
    store.dispatch(showSnackbar("Lorem ipsum dolor met.", 'success'));

    let state = store.getState().snackbar;
    assert.deepEqual(state, {
      type: 'success',
      message: "Lorem ipsum dolor met.",
      isVisible: true
    }, "message was set on state");
  });

  it("hideSnackbar action hides message", function() {
    store.dispatch(showSnackbar("Lorem ipsum dolor met.", 'success'));
    store.dispatch(hideSnackbar());

    let state = store.getState().snackbar;
    assert.ok(!state.isVisible, "visible flag was removed");
  });
});
