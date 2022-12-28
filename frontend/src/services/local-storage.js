let storage = window.localStorage

export class LocalStorage {
  init(prefix) {
    this._prefix = prefix
    this._watchers = []

    window.addEventListener("storage", (e) => {
      let newValueJson = JSON.parse(e.newValue)
      this._watchers.forEach(function (watcher) {
        if (watcher.key === e.key && e.oldValue !== e.newValue) {
          watcher.callback(newValueJson)
        }
      })
    })
  }

  set(key, value) {
    storage.setItem(this._prefix + key, JSON.stringify(value))
  }

  get(key) {
    let itemString = storage.getItem(this._prefix + key)
    if (itemString) {
      return JSON.parse(itemString)
    } else {
      return null
    }
  }

  watch(key, callback) {
    this._watchers.push({
      key: this._prefix + key,
      callback: callback,
    })
  }
}

export default new LocalStorage()
