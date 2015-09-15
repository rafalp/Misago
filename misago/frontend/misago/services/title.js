(function (Misago) {
  'use strict';

  var PageTitle = function(forum_name) {
    this.set = function(title) {
      if (title) {
        this._set_complex(title);
      } else {
        document.title = forum_name;
      }
    };

    this._set_complex = function(title) {
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

      document.title = completeTitle + ' | ' + forum_name;
    };
  };

  Misago.addService('page-title', function(_) {
    _.title = new PageTitle(_.settings.forum_name)
  });
}(Misago.prototype));
