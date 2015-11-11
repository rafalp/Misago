(function (Misago) {
  'use strict';

  var email = {
    controller: function(_) {
      _.auth.denyAnonymous(
        gettext("You have to be signed in to change your options."));

      this.container.title.set({
        title: gettext("E-mail"),
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

  Misago.addService('route:options:email', function(_) {
    _.route('options-email', email);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));
