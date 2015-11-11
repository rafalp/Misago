(function (Misago) {
  'use strict';

  var index = {
    controller: function(_) {
      _.auth.denyAnonymous(
        gettext("You have to be signed in to change your options."));

      _.router.redirect('options_forum');
    }
  };

  Misago.addService('route:options', function(_) {
    _.route('options', index);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));
