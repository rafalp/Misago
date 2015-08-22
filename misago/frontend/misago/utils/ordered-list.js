(function (ns) {
  'use strict';

  ns.OrderedList = function(items) {
    this.is_ordered = false;
    this._items = items || [];

    this.add = function(key, item, order) {
      this._items.push({
        key: key,
        item: item,
        after: ns.get(order, 'after'),
        before: ns.get(order, 'before')
      });
    };

    this.get = function(key, value) {
      for (var i = 0; i < this._items.length; i++) {
        if (this._items[i].key === key) {
          return this._items[i].item;
        }
      }

      return value;
    };

    this.has = function(key) {
      return this.get(key) !== undefined;
    };

    this.values = function() {
      var values = [];
      for (var i = 0; i < this._items.length; i++) {
        values.push(this._items[i].item);
      }
      return values;
    };

    this.order = function(values_only) {
      if (!this.is_ordered) {
        this._items = this._order(this._items);
        this.is_ordered = true;
      }

      if (values_only || typeof values_only === 'undefined') {
        return this.values();
      } else {
        return this._items;
      }
    };

    this._order = function(unordered) {
      // Index of unordered items
      var index = [];
      unordered.forEach(function (item) {
        index.push(item.key);
      });

      // Ordered items
      var ordered = [];
      var ordering = [];

      // First pass: register items that
      // don't specify their order
      unordered.forEach(function (item) {
        if (!item.after && !item.before) {
          ordered.push(item);
          ordering.push(item.key);
        }
      });

      // Second pass: keep iterating items
      // until we hit iterations limit or finish
      // ordering list
      function insertItem(item) {
        var insertAt = -1;
        if (ordering.indexOf(item.key) === -1) {
          if (item.after) {
            insertAt = ordering.indexOf(item.after);
            if (insertAt !== -1) {
              insertAt += 1;
            }
          } else if (item.before) {
            insertAt = ordering.indexOf(item.before);
          }

          if (insertAt !== -1) {
            ordered.splice(insertAt, 0, item);
            ordering.splice(insertAt, 0, item.key);
          }
        }
      }

      var iterations = 200;
      while (iterations > 0 && index.length !== ordering.length) {
        iterations -= 1;
        unordered.forEach(insertItem);
      }

      return ordered;
    };
  };
} (Misago.prototype));
