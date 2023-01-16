class OrderedList {
  constructor(items) {
    this.isOrdered = false
    this._items = items || []
  }

  add(key, item, order) {
    this._items.push({
      key: key,
      item: item,

      after: order ? order.after || null : null,
      before: order ? order.before || null : null,
    })
  }

  get(key, value) {
    for (var i = 0; i < this._items.length; i++) {
      if (this._items[i].key === key) {
        return this._items[i].item
      }
    }

    return value
  }

  has(key) {
    return this.get(key) !== undefined
  }

  values() {
    var values = []
    for (var i = 0; i < this._items.length; i++) {
      values.push(this._items[i].item)
    }
    return values
  }

  order(values_only) {
    if (!this.isOrdered) {
      this._items = this._order(this._items)
      this.isOrdered = true
    }

    if (values_only || typeof values_only === "undefined") {
      return this.values()
    } else {
      return this._items
    }
  }

  orderedValues() {
    return this.order(true)
  }

  _order(unordered) {
    // Index of unordered items
    var index = []
    unordered.forEach(function (item) {
      index.push(item.key)
    })

    // Ordered items
    var ordered = []
    var ordering = []

    // First pass: register items that
    // don't specify their order
    unordered.forEach(function (item) {
      if (!item.after && !item.before) {
        ordered.push(item)
        ordering.push(item.key)
      }
    })

    // Second pass: register items that
    // specify their before to "_end"
    unordered.forEach(function (item) {
      if (item.before === "_end") {
        ordered.push(item)
        ordering.push(item.key)
      }
    })

    // Third pass: keep iterating items
    // until we hit iterations limit or finish
    // ordering list
    function insertItem(item) {
      var insertAt = -1
      if (ordering.indexOf(item.key) === -1) {
        if (item.after) {
          insertAt = ordering.indexOf(item.after)
          if (insertAt !== -1) {
            insertAt += 1
          }
        } else if (item.before) {
          insertAt = ordering.indexOf(item.before)
        }

        if (insertAt !== -1) {
          ordered.splice(insertAt, 0, item)
          ordering.splice(insertAt, 0, item.key)
        }
      }
    }

    var iterations = 200
    while (iterations > 0 && index.length !== ordering.length) {
      iterations -= 1
      unordered.forEach(insertItem)
    }

    return ordered
  }
}

export default OrderedList
