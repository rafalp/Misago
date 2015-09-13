(function (Misago) {
  'use strict';

  var Api = function(_) {
    this.buildUrl = function(model, call, querystrings) {
      var url = _.router.baseUrl;
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
