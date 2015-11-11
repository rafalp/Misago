(function (Misago) {
  'use strict';

  Misago.Page = function(name, _) {
    var self = this;

    this.name = name;
    this.isFinalized = false;
    this._sections = [];

    var finalize = function() {
      if (!self.isFinalized) {
        self.isFinalized = true;

        var visible = [];
        self._sections.forEach(function (item) {
          if (!item.visibleIf || item.visibleIf(_)) {
            visible.push(item);
          }
        });
        self._sections = new Misago.OrderedList(visible).order(true);
      }
    };

    this.addSection = function(section) {
      if (this.isFinalized) {
        throw (this.name + " page was initialized already and no longer accepts new sections");
      }

      this._sections.push({
        key: section.link,
        item: section,

        after: section.after,
        before: section.before
      });
    };

    this.getSections = function() {
      finalize();
      return this._sections;
    };

    this.getDefaultLink = function() {
      finalize();
      return this._sections[0].link;
    };
  };
}(Misago.prototype));
