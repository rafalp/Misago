(function (ns) {
  'use strict';

  ns.PageTitle = function(_) {
    _._setTitle = function(title) {
      if (typeof title === 'string') {
        title = {title: title};
      }

      var complete_title = title.title;

      if (typeof title.page !== 'undefined' && title.page > 1) {
        complete_title += ' (' + interpolate(gettext('page %(page)s'), { page:title.page }, true) + ')';
      }

      if (typeof title.parent !== 'undefined') {
        complete_title += ' | ' + title.parent;
      }

      document.title = complete_title + ' | ' + this.settings.forum_name;
    };

    _.setTitle = function(title) {
      if (title) {
        this._setTitle(title);
      } else {
        document.title = this.settings.forum_name;
      }
    };
  };
}(Misago.prototype));
