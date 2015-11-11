(function (Misago) {
  'use strict';

  var forum = {
    controller: function(_) {
      _.auth.denyAnonymous(
        gettext("You have to be signed in to change your options."));

      this.container.title.set({
        title: gettext("Forum options"),
        parent: gettext("Options")
      });
    },
    view: function(ctrl, _) {
      return m('.page.page-options.page-forum-options', [
        _.component('header', {
          title: gettext("Options")
        }),
        m('.container',
          m('p', 'Lorem ipsum dolor met.')
        )
      ]);
    }
  };

  Misago.addService('route:options:forum', function(_) {
    _.route('options-forum', forum);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));
