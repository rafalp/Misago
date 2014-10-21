MisagoStorage = function() {

  this.has = function(key) {
    return localStorage.getItem(key) !== null;
  }

  this.get = function(key, value) {

    if (this.has(key)) {
      return localStorage.getItem(key);
    } else if (value !== null) {
      return value;
    } else {
      return null;
    }

  }

  this.set = function(key, value) {
    localStorage.setItem(key, value)
    return value;
  }

  this.pop = function(key, value) {

    value = localStorage.getItem(key, value);
    localStorage.removeItem(key);
    return value;

  }

}


MisagoDummyStorage = function() {

  this.has = function(key) {
    return false
  }

  this.get = function(key, value) {

    if (value !== undefined) {
      return value;
    } else {
      return null;
    }

  }

  this.set = function(key, value) {
    return false;
  }

  this.pop = function(key, value) {

    if (value !== undefined) {
      return value;
    } else {
      return null;
    }

  }

}


if (localStorage !== undefined) {
  Misago.Storage = new MisagoStorage();
} else {
  Misago.Storage = new MisagoDummyStorage();
}
