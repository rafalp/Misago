(function (Misago) {
  'use strict';

  var style = '.well.well-form.well-form-request-activation-link';

  var ViewModel = function(api) {
    this.api = api;
    this.user = null;

    this.success = function(user) {
      this.user = user;
    };

    this.error = function(rejection, _) {
      if (rejection.code === 'already_active') {
        _.alert.info(rejection.detail);
        _.modal('sign-in');
      } else if (rejection.code === 'inactive_admin') {
        _.alert.info(rejection.detail);
      } else {
        _.alert.error(rejection.detail);
      }
    };

    this.reset = function() {
      this.user = null;
    };
  };

  var form = {
    controller: function(_) {
      var vm = new ViewModel(_.context.SEND_ACTIVATION_API);

      return {
        vm: vm,
        form: _.form('request-link', vm)
      };
    },
    view: function(ctrl, _) {
      if (ctrl.vm.user) {
        return this.done(ctrl.vm, ctrl.form, _);
      } else {
        return this.form(ctrl.form, _);
      }
    },
    done: function(vm, form, _) {
      var message = gettext("Activation link sent to %(email)s.");

      return m(style + '.well-done',
        m('.done-message', [
          m('.message-icon',
            m('span.material-icon', 'check')
          ),
          m('.message-body',
            m('p',
              interpolate(message, {
                email: vm.user.email
              }, true)
            )
          ),
          _.component('button', {
            class: '.btn-default.btn-block',
            submit: false,
            label: gettext("Request another link"),
            onclick: form.reset.bind(form)
          })

        ])
      );
    },
    form: function(form, _) {
      return m(style,
        m('form', {onsubmit: form.submit}, [
          m('.form-group',
            m('.control-input',
              Misago.input({
                disabled: form.isBusy,
                value: form.email,
                placeholder: gettext("Your e-mail address")
              })
            )
          ),
          _.component('button', {
            class: '.btn-primary.btn-block',
            submit: true,
            loading: form.isBusy,
            label: gettext("Send link")
          })
        ])
      );
    }
  };

  Misago.addService('component:request-activation-link-form', function(_) {
    _.component('request-activation-link-form', form);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
