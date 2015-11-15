(function (Misago) {
  'use strict';

  var style = '.well.well-form.well-form-reset-password';

  var ViewModel = function(api) {
    this.api = api;

    this.success = function(user, _) {
      _.auth.signOut();
      _.mountPage(_.component('forgotten-password:done-page', user));
    };
  };

  var component = {
    controller: function(_) {
      var vm = new ViewModel(_.context.CHANGE_PASSWORD_API_URL);

      return {
        form: _.form('reset-password', vm)
      };
    },
    view: function(ctrl, _) {
      return m(style,
        m('form', {onsubmit: ctrl.form.submit}, [
          m('.form-group',
            m('.control-input',
              Misago.input({
                disabled: ctrl.form.isBusy,
                value: ctrl.form.password,
                type: 'password',
                placeholder: gettext("Enter new password")
              })
            )
          ),
          _.component('button', {
            class: '.btn-primary.btn-block',
            submit: true,
            loading: ctrl.form.isBusy,
            label: gettext("Change password")
          })
        ])
      );
    }
  };

  Misago.addService('component:forgotten-password:reset-password', function(_) {
    _.component('forgotten-password:reset-password', component);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
