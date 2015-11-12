(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var signin = {
    controller: function(_) {
      return {
        form: _.form('sign-in')
      };
    },
    view: function(ctrl, _) {
      var activateButton = null;

      if (ctrl.form.showActivation) {
        activateButton = m('a.btn.btn-block.btn-success',
          {href: _.context.REQUEST_ACTIVATION_URL},
          gettext("Activate account")
        );
      }

      return m('.modal-dialog.modal-sm.modal-signin[role="document"]',
        {config: persistent},
        m('.modal-content', [
          _.component('modal:header', gettext("Sign in")),
          m('form', {onsubmit: ctrl.form.submit}, [
            m('.modal-body', [
              m('.form-group',
                m('.control-input',
                  Misago.input({
                    disabled: ctrl.form.isBusy,
                    value: ctrl.form.username,
                    placeholder: gettext("Username or e-mail")
                  })
                )
              ),
              m('.form-group',
                m('.control-input',
                  Misago.input({
                    type: 'password',
                    disabled: ctrl.form.isBusy,
                    value: ctrl.form.password,
                    placeholder: gettext("Password")
                  })
                )
              )
            ]),
            m('.modal-footer', [
              activateButton,
              _.component('button', {
                class: '.btn-primary.btn-block',
                submit: true,
                loading: ctrl.form.isBusy,
                label: gettext("Sign in")
              }),
              m('a.btn.btn-block.btn-default',
                {href: _.context.FORGOTTEN_PASSWORD_URL},
                gettext("Forgot password?")
              )
            ])
          ])
        ])
      );
    }
  };

  Misago.addService('modal:sign-in', function(_) {
    _.modal('sign-in', signin);
  },
  {
    after: 'modals'
  });
}(Misago.prototype));
