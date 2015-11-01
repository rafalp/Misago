(function (Misago) {
  'use strict';

  var form = {
    view: function(ctrl, form, _) {
      return m('.well.well-form',
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

  Misago.addService('component:request-link-form', function(_) {
    _.component('request-link-form', form);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
