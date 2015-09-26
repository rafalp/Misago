(function (Misago) {
  'use strict';

  var filtersUrl = function(filters) {
    if (typeof filters === 'object') {
      var values = [];
      for (var key in filters) {
        if (filters.hasOwnProperty(key)) {
          var encodedKey = encodeURIComponent(key);
          var encodedValue = encodeURIComponent(filters[key]);
          values.push(encodedKey + '=' + encodedValue);
        }
      }
      return '?' + values.join('&');
    } else {
      return filters + '/';
    }
  };

  var Query = function(_, call) {
    this.url = call.url || _.setup.api;

    if (call.path) {
      this.url += call.path + '/';
    } else if (call.related) {
      this.url += call.related + '/';
    } else {
      this.url += call.model + 's' + '/';
    }

    if (call.filters) {
      this.url += filtersUrl(call.filters);
    }

    if (!call.url && call.filters) {
      if (call.model) {
        this.related = function(model, filters) {
          return new Query(_, {
            url: this.url,
            relation: call.model,
            related: model,
            filters: filters,
          });
        };
      }

      this.endpoint = function(path, filters) {
        return new Query(_, {
          url: this.url,
          path: path,
          filters: filters
        });
      };
    }

    this.get = function() {
      var model = null;
      if (call.related) {
        model = call.relation + ':' + call.related;
      } else if (call.model) {
        model = call.model;
      }

      return _.ajax.get(this.url).then(function(data) {
        if (model) {
          if (data.results) {
            data.results.map(function(item) {
              return _.models.new(model, item);
            });
            return data;
          } else {
            return _.models.new(model, data);
          }
        } else {
          return data;
        }
      });
    };

    this.post = function(data) {
      return _.ajax.post(this.url, data);
    };

    this.patch = function(data) {
      return _.ajax.patch(this.url, data);
    };

    this.put = function(data) {
      return _.ajax.put(this.url, data);
    };

    this.delete = function() {
      return _.ajax.delete(this.url);
    };

    // shortcut for get()
    this.then = function(resolve, reject) {
      return this.get().then(resolve, reject);
    };
  };

  var Api = function(_) {
    this.model = function(model, filters) {
      return new Query(_, {
        model: model,
        filters: filters,
      });
    };

    this.endpoint = function(path, filters) {
      return new Query(_, {
        path: path,
        filters: filters
      });
    };
  };

  Misago.addService('api', function(_) {
    return new Api(_);
  });
}(Misago.prototype));
