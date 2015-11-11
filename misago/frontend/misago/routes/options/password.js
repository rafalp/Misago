(function (Misago) {
  'use strict';

  var password = {
    controller: function(_) {
      _.auth.denyAnonymous(
        gettext("You have to be signed in to change your options."));

      this.container.title.set({
        title: gettext("Password"),
        parent: gettext("Options")
      });
    },
    view: function(ctrl, _) {
      return m('.page.page-options.page-forum-options', [
        _.component('header', {
          title: gettext("Change options")
        }),
        m('.container',
          m('p', 'Lorem ipsum dolor met.')
        )
      ]);
    }
  };

  Misago.addService('route:options:password', function(_) {
    _.route('options-password', password);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));
