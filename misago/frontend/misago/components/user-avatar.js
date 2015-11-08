(function (Misago) {
  'use strict';

  var avatar = {
    defaultSize: 100,

    src: function(user, size, _) {
      var src = _.router.baseUrl + 'user-avatar/';

      if (user && user.id) {
        // just avatar hash, size and user id
        src += user.avatar_hash + '/' + size + '/' + user.id + '.png';
      } else {
        // just append avatar size to file to produce no-avatar placeholder
        src += size + '.png';
      }

      return src;
    },
    view: function(ctrl, user, size, _) {
      var finalSize = size || this.defaultSize;
      return m('img', {
        alt: user && user.username ? user.username : gettext("Unregistered"),
        width: finalSize,
        height: finalSize,
        src: this.src(user, finalSize, _)
      });
    }
  };

  Misago.addService('component:user-avatar', function(_) {
    _.component('user-avatar', avatar);
  },
  {
    after: 'components'
  });
} (Misago.prototype));
