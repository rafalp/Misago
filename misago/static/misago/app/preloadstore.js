window.MisagoPreloadStore = {

  data: {},

  has: function(key) {
    return this.data.hasOwnProperty(key);
  },

  get: function(key, value) {

    if (this.has(key)) {
      return this.data[key];
    } else if (value !== undefined) {
      return value;
    } else {
      return undefined;
    }

  },

  set: function(key, value) {
    this.data[key] = value;
    return value;
  }

}
