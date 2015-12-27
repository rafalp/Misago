import assert from 'assert';
import { StoreWrapper } from 'misago/services/store';
import reducer, { initialState, showSnackbar, hideSnackbar } from 'misago/reducers/snackbar';
import { Snackbar } from 'misago/services/snackbar';

var store, snackbar = null;

describe("Snackbar", function() {
  beforeEach(function() {
    store = new StoreWrapper();
    store.addReducer('snackbar', reducer, initialState);
    store.init();

    snackbar = new Snackbar();
    snackbar.init(store);
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

  it("sets message in store", function() {
    snackbar.alert("Lorem ipsum dolor met sit amet.", 'warning');

    let state = store.getState().snackbar;
    assert.deepEqual(state, {
      type: 'warning',
      message: "Lorem ipsum dolor met sit amet.",
      isVisible: true
    }, "service set message in store");
  });

  it("provides shortcut for setting info message", function() {
    snackbar.info("Lorem ipsum dolor met sit amet.");

    let state = store.getState().snackbar;
    assert.deepEqual(state, {
      type: 'info',
      message: "Lorem ipsum dolor met sit amet.",
      isVisible: true
    }, "service set info message in store");
  });

  it("provides shortcut for setting warning message", function() {
    snackbar.warning("Lorem ipsum dolor met sit amet.");

    let state = store.getState().snackbar;
    assert.deepEqual(state, {
      type: 'warning',
      message: "Lorem ipsum dolor met sit amet.",
      isVisible: true
    }, "service set warning message in store");
  });

  it("provides shortcut for setting error message", function() {
    snackbar.error("Lorem ipsum dolor met sit amet.");

    let state = store.getState().snackbar;
    assert.deepEqual(state, {
      type: 'error',
      message: "Lorem ipsum dolor met sit amet.",
      isVisible: true
    }, "service set error message in store");
  });

  it("provides shortcut for setting success message", function() {
    snackbar.success("Lorem ipsum dolor met sit amet.");

    let state = store.getState().snackbar;
    assert.deepEqual(state, {
      type: 'success',
      message: "Lorem ipsum dolor met sit amet.",
      isVisible: true
    }, "service set success message in store");
  });
});
