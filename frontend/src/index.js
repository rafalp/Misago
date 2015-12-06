import OrderedList from 'misago/utils/ordered-list';

export class Misago {
  constructor() {
    this._initializers = [];
  }

  addInitializer(initializer) {
    this._initializers.push({
      key: initializer.name,

      item: initializer.init,

      after: initializer.after,
      before: initializer.before
    });
  }

  init(options) {
    var initOrder = new OrderedList(this._initializers).orderedValues();
    initOrder.forEach(function(initializer) {
      initializer(options);
    });
  }
}

// create  singleton
var misago = new Misago();

// expose it globally
global.misago = misago;

// and export it for tests and stuff
export default misago;
