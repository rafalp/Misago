export default class {
  constructor(callback, count) {
    this._callback = callback
    this._count = count
  }

  count() {
    this._count -= 1
    if (this._count === 0) {
      this._callback()
    }
  }
}
