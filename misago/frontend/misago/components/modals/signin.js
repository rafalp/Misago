(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var signin = {
    controller: function() {
      return {
        busy: m.prop(false),
        showActivation: m.prop(false),

        username: m.prop(''),
        password: m.prop(''),

        validation: {
          'username': [Misago.validators.required()],
          'password': [Misago.validators.required()]
        }
      };
    },
    submit: function(ctrl, _) {
      if (ctrl.busy()) {
        return false;
      }

      if (_.validate(ctrl).length) {
        _.alert.error(gettext("Fill out both fields."));
        return false;
      }

      m.startComputation();
      ctrl.busy(true);
      m.endComputation();

      var credentials = {
        username: ctrl.username(),
        password: ctrl.password()
      };

      var self = this;

      _.api.endpoint('auth').post(credentials).then(
      function() {
        self.success(credentials, _);
      },
      function(error) {
        self.error(ctrl, error, _);
      }).then(function() {
        m.startComputation();
        ctrl.busy(false);
        m.endComputation();
      });

      return false;
    },
    success: function(credentials, _) {
      var $form = $('#hidden-login-form');

      // refresh CSRF token because parent api call changed it
      _.ajax.refreshCsrfToken();

      // fill out form with user credentials and submit it, this will tell
      // misago to redirect user back to right page, and will trigger browser's
      // key ring feature
      $form.find('input[name=csrf_token]').val(_.ajax.csrfToken);
      $form.find('input[name=redirect_to]').val(window.location.href);
      $form.find('input[name=username]').val(credentials.username);
      $form.find('input[name=password]').val(credentials.password);
      $form.submit();
    },
    error: function(ctrl, rejection, _) {
      if (rejection.status === 400) {
        if (rejection.code === 'inactive_admin') {
          _.alert.info(rejection.detail);
        } else if (rejection.code === 'inactive_user') {
          _.alert.info(rejection.detail);
          ctrl.showActivation(true);
        } else if (rejection.code === 'banned') {
          // handle ban!
        } else {
          _.alert.error(rejection.detail);
        }
      } else {
        _.api.alert(rejection);
      }
    },
    view: function(ctrl, _) {
      return m('.modal-dialog.modal-sm.modal-signin[role="document"]',
        {config: persistent},
        m('.modal-content', [
          _.component('modal:header', gettext('Sign in')),
          m('form', {onsubmit: this.submit.bind(this, ctrl, _)}, [
            m('.modal-body', [
              m('.form-group',
                m('.control-input',
                  Misago.input({
                    disabled: ctrl.busy(),
                    value: ctrl.username,
                    placeholder: gettext("Username or e-mail")
                  })
                )
              ),
              m('.form-group',
                m('.control-input',
                  Misago.input({
                    type: 'password',
                    disabled: ctrl.busy(),
                    value: ctrl.password,
                    placeholder: gettext("Password")
                  })
                )
              )
            ]),
            m('.modal-footer',
              _.component('button', {
                class: '.btn-primary.btn-block',
                submit: true,
                loading: ctrl.busy(),
                label: gettext('Sign in')
              })
            )
          ])
        ])
      );
    }
  };

  Misago.addService('modal:sign-in', {
    factory: function(_) {
      _.modal('sign-in', signin);
    },
    after: 'modals'
  });
}(Misago.prototype));
