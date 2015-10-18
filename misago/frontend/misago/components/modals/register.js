(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var register = {
    controller: function(_) {
      return {
        form: _.form('register')
      };
    },
    view: function(ctrl, _) {
      var captcha = _.captcha.component({
        form: ctrl.form,

        labelClass: '.col-md-4',
        controlClass: '.col-md-8'
      });

      var footnote = null;
      var termsUrl = _.settings.terms_of_service_link;

      if (!termsUrl && _.settings.terms_of_service) {
        termsUrl = _.router.url('terms_of_service');
      }

      if (termsUrl) {
        footnote = m('a', {href: termsUrl},
          m.trust(interpolate(gettext("By registering you agree to site's %(terms)s."), {
            terms: '<strong>' + gettext("terms and conditions") + '</strong>'
          }, true))
        );
      }

      return m('.modal-dialog.modal-form.modal-register[role="document"]',
        {config: persistent},
        m('.modal-content', [
          _.component('modal:header', gettext('Register')),
          m('form.form-horizontal',
          {
            onsubmit: ctrl.form.submit
          },
          [
            m('input[type="text"]', {
              name:'_username',
              style: 'display: none'
            }),
            m('input[type="password"]', {
              name:'_password',
              style: 'display: none'
            }),
            m('.modal-body', [
              _.component('form-group', {
                label: gettext("Username"),
                labelClass: '.col-md-4',
                controlClass: '.col-md-8',
                control: _.input({
                  value: _.validate(ctrl.form, 'username'),
                  id: 'id_username',
                  disabled: ctrl.form.isBusy
                }),
                validation: ctrl.form.errors,
                validationKey: 'username'
              }),
              _.component('form-group', {
                label: gettext("E-mail"),
                labelClass: '.col-md-4',
                controlClass: '.col-md-8',
                control: _.input({
                  value: _.validate(ctrl.form, 'email'),
                  id: 'id_email',
                  disabled: ctrl.form.isBusy
                }),
                validation: ctrl.form.errors,
                validationKey: 'email'
              }),
              _.component('form-group', {
                label: gettext("Password"),
                labelClass: '.col-md-4',
                controlClass: '.col-md-8',
                control: _.input({
                  value: _.validate(ctrl.form, 'password'),
                  type: 'password',
                  id: 'id_password',
                  disabled: ctrl.form.isBusy
                }),
                validation: ctrl.form.errors,
                validationKey: 'password',
                helpText: _.component('password-strength', {
                  inputs: [
                    ctrl.form.username(),
                    ctrl.form.email()
                  ],
                  password: ctrl.form.password()
                })
              }),
              captcha
            ]),
            m('.modal-footer', [
              footnote,
              _.component('button', {
                class: '.btn-primary',
                submit: true,
                loading: ctrl.form.isBusy,
                label: gettext("Register account")
              })
            ])
          ])
        ])
      );
    }
  };

  Misago.addService('modal:register', function(_) {
    _.modal('register', register);
  },
  {
    after: 'modals'
  });
}(Misago.prototype));
