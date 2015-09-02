(function (Misago) {
  'use strict';

  Misago.PageTitle = function(_) {
    _._setTitle = function(title) {
      if (typeof title === 'string') {
        title = {title: title};
      }

      var completeTitle = title.title;

      if (typeof title.page !== 'undefined' && title.page > 1) {
        completeTitle += ' (' + interpolate(gettext('page %(page)s'), { page:title.page }, true) + ')';
      }

      if (typeof title.parent !== 'undefined') {
        completeTitle += ' | ' + title.parent;
      }

      document.title = completeTitle + ' | ' + this.settings.forum_name;
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
