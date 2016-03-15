import assert from 'assert';
import { StoreWrapper } from 'misago/services/store';
import reducer, { initialState } from 'misago/reducers/snackbar';
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

  it("provides shortcut for backend disconnection", function() {
    snackbar.apiError({
      status: 0,
      detail: "You got disconnected!"
    });

    assert.deepEqual(store.getState().snackbar, {
      type: 'error',
      message: "You got disconnected!",
      isVisible: true
    }, "service set disconnected message in store");
  });

  it("provides shortcut for backend permission denied", function() {
    snackbar.apiError({
      status: 403,
      detail: "Permission denied"
    });

    assert.deepEqual(store.getState().snackbar, {
      type: 'error',
      message: "You don't have permission to perform this action.",
      isVisible: true
    }, "service set default 403 message in store");
  });

  it("provides shortcut for custom backend permission denied", function() {
    snackbar.apiError({
      status: 403,
      detail: "REJECTION!"
    });

    assert.deepEqual(store.getState().snackbar, {
      type: 'error',
      message: "REJECTION!",
      isVisible: true
    }, "service set custom 403 message in store");
  });

  it("provides shortcut for backend rejection", function() {
    snackbar.apiError({
      status: 400,
      detail: "NOPE!"
    });

    assert.deepEqual(store.getState().snackbar, {
      type: 'error',
      message: "NOPE!",
      isVisible: true
    }, "service set custom 400 message in store");
  });

  it("provides shortcut for backend 404 error", function() {
    snackbar.apiError({
      status: 404,
      detail: "NOT FOUND"
    });

    assert.deepEqual(store.getState().snackbar, {
      type: 'error',
      message: "NOT FOUND",
      isVisible: true
    }, "service set not found message in store");
  });
});
