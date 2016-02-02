import OrderedList from 'misago/utils/ordered-list';

export class Misago {
  constructor() {
    this._initializers = [];
    this._context = {};
  }

  addInitializer(initializer) {
    this._initializers.push({
      key: initializer.name,

      item: initializer.initializer,

      after: initializer.after,
      before: initializer.before
    });
  }

  init(context) {
    this._context = context;

    var initOrder = new OrderedList(this._initializers).orderedValues();
    initOrder.forEach(initializer => {
      initializer(this);
    });
  }

  // context accessors
  has(key) {
    return !!this._context[key];
  }

  get(key, fallback) {
    if (this.has(key)) {
      return this._context[key];
    } else {
      return fallback || undefined;
    }
  }

  pop(key) {
    if (this.has(key)) {
      let value = this._context[key];
      this._context[key] = null;
      return value;
    } else {
      return undefined;
    }
  }
}

// create  singleton
var misago = new Misago();

// expose it globally
global.misago = misago;

// and export it for tests and stuff
export default misago;
