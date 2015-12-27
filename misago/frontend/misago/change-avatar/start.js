(function (Misago) {
  'use strict';

  var component = {
    view: function(ctrl, vm, _) {
      var options = [];

      if (vm.options.gravatar) {
        options.push(
          _.component('button', {
            class: '.btn-default.btn-block',
            onclick: vm.downloadGravatar,
            label: gettext("Download my Gravatar")
          })
        );
      }

      options.push(
        _.component('button', {
          class: '.btn-default.btn-block',
          onclick: vm.generateAvatar,
          label: gettext("Generate my individual avatar")
        })
      );

      return m('.modal-body.modal-avatar-options',
        m('.row', [
          m('.col-md-4',
            _.component('user-avatar', vm.user, 200)
          ),
          m('.col-md-8',
            m('ul.list-unstyled',
              options.map(function(item) {
                return m('li',
                  item
                );
              })
            )
          )
        ])
      );
    }
  };

  Misago.addService('component:change-avatar:start', function(_) {
    _.component('change-avatar:start', component);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
