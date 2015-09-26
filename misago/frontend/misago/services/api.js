(function (Misago) {
  'use strict';

  var Query = function(_, model) {

  };

  var Api = function(_) {
    var apiRoot = _.setup.api;

    this.buildUrl = function(model, call, querystrings) {
      var url = _.setup.api;
      url += 'api/' + model + '/';
      return url;
    };

    this.one = function(model, id) {
      var url = this.buildUrl(model) + id + '/';
      return _.ajax.get(url);
    };

    this.many = function(model, filters) {

    };

    this.call = function(model, target, call, data) {

    };
  };

  Misago.addService('api', function(_) {
    return new Api(_);
  });
}(Misago.prototype));
