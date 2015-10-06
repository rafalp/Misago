(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var signin = {
    controller: function() {
      return {
        busy: m.prop(false),

        username: m.prop(''),
        password: m.prop(''),
      };
    },
    submit: function(_) {
      if (this.busy()) {
        return false;
      }

      m.startComputation();
      this.busy(true);
      m.endComputation();

      var credentials = {
        username: $.trim(this.username()),
        password: $.trim(this.password())
      };

      var self = this;

      _.api.endpoint('auth').post(credentials).then(
      function(data) {
        console.log(data);
      },
      function(error) {
        console.log(error);
      }).then(function() {
        m.startComputation();
        self.busy(false);
        m.endComputation();
      });

      return false;
    },
    view: function(ctrl, _) {
      return m('.modal-dialog.modal-sm.modal-signin[role="document"]',
        {config: persistent},
        m('.modal-content', [
          _.component('modal:header', gettext('Sign in')),
          m('form', {onsubmit: this.submit.bind(ctrl, _)}, [
            m('.modal-body', [
              m('.form-group',
                m('.control-input',
                  Misago.input({
                    disabled: ctrl.busy(),
                    value: ctrl.password,
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
            m('.modal-footer', [
              m('button.btn.btn-primary.btn-block[type="submit"]',
                ctrl.busy() ? 'Working!!!' : gettext('Sign in')
              )
            ])
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
