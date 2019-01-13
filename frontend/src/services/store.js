import { combineReducers, createStore } from "redux"

export class StoreWrapper {
  constructor() {
    this._store = null
    this._reducers = {}
    this._initialState = {}
  }

  addReducer(name, reducer, initialState) {
    this._reducers[name] = reducer
    this._initialState[name] = initialState
  }

  init() {
    this._store = createStore(
      combineReducers(this._reducers),
      this._initialState
    )
  }

  getStore() {
    return this._store
  }

  // Store API

  getState() {
    return this._store.getState()
  }

  dispatch(action) {
    return this._store.dispatch(action)
  }
}

export default new StoreWrapper()
