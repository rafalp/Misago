(function (Misago) {
  'use strict';

  Misago.addService('page-title', function(_) {
    var setPageTitle = function(_, title) {
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

      document.title = completeTitle + ' | ' + _.settings.forum_name;
    };

    _.setTitle = function(title) {
      if (title) {
        setPageTitle(this, title);
      } else {
        document.title = this.settings.forum_name;
      }
    };
  });
}(Misago.prototype));
