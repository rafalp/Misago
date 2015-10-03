(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var signin = Misago.route({
    controller: function() {
      console.log('construct!');
      return {
        busy: false,

        username: m.prop(''),
        password: m.prop(''),

        validate: function() {
          return false;
        },

        submit: function(e) {
          console.log('SUBMITTING FORM!');
          return false;
        }
      };
    },
    view: function(ctrl) {
      return m('.modal-dialog.modal-sm.modal-signin[role="document"]',
        {config: persistent},
        m('.modal-content',
          m('form', {onsubmit: ctrl.submit}, [
            m('.modal-header',
              m('button.close[type="button"]',
                {'data-dismiss': 'modal', 'aria-label': gettext('Close')},
                m('span', {'aria-hidden': 'true'}, m.trust('&times;'))
              ),
              m('h4#misago-modal-label.modal-title', 'Sign in')
            ),
            m('.modal-body', [
              m('.form-group',
                m('.control-input',
                  m('input.form-control[type="text"]', {
                    placeholder: gettext("Username or e-mail"),
                    oninput: m.withAttr('value', ctrl.username),
                    value: ctrl.username()
                  })
                )
              ),
              m('.form-group',
                m('.control-input',
                  m('input.form-control[type="password"]', {
                    placeholder: gettext("Password"),
                    oninput: m.withAttr('value', ctrl.password),
                    value: ctrl.password()
                  })
                )
              )
            ]),
            m('.modal-footer', [
              m('button.btn.btn-primary.btn-block[type="submit"]',
                gettext('Sign in')
              )
            ])
          ])
        )
      );
    }
  });

  Misago.addService('component:modal:sign-in', {
    factory: function(_) {
      _.component('modal:sign-in', signin);
    },
    after: 'components'
  });
}(Misago.prototype));
