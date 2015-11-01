(function (Misago) {
  'use strict';

  var ViewModel = function() {
    this.endpoint = 'send-password-form';
    this.user = null;

    this.activation = null;
    this.activationMessage = null;

    this.success = function(user) {
      this.user = user;
    };

    this.error = function(rejection, _) {
      if (['inactive_user', 'inactive_admin'].indexOf(rejection.code) > -1) {
        this.activation = rejection.code;
        this.activationMessage = rejection.detail;
      } else {
        _.alert.error(rejection.detail);
      }
    };

    this.reset = function() {
      this.user = null;
      this.activation = null;
      this.activationMessage = null;
    };
  };

  var requestPasswordChange = {
    controller: function(_) {
      _.title.set(gettext("Change forgotten password"));

      var vm = new ViewModel();

      return {
        vm: vm,
        form: _.form('request-link', vm)
      };
    },
    view: function(ctrl, _) {
      if (ctrl.vm.user) {
        return this.completed(ctrl.form, ctrl.vm, _);
      } else if (ctrl.vm.activation) {
        return this.inactive(ctrl.form, ctrl.vm, _);
      } else {
        return this.form(ctrl.form, _);
      }
    },
    completed: function(form, vm, _) {
      var message = gettext("%(username)s, we have sent link to your password change form to %(email)s.");

      return m('.page.page-message.page-message-success',
        m('.container',
          m('.message-panel', [
            m('.message-icon',
              m('span.material-icon', 'check')
            ),
            m('.message-body', [
              m('p.lead',
                gettext("Change password form link sent.")
              ),
              m('p',
                interpolate(message, {
                  username: vm.user.username,
                  email: vm.user.email
                }, true)
              ),
              m('p',
                _.component('button', {
                  class: '.btn-default',
                  submit: false,
                  label: gettext("Request another link"),
                  onclick: form.reset.bind(form)
                })
              )
            ])
          ])
        )
      );
    },
    inactive: function(form, vm, _) {
      var activateButton = null;

      if (vm.activation === 'inactive_user') {
        activateButton = m('a.btn.btn-primary',
          {href: _.router.url('request_activation')},
          gettext("Activate account")
        );
      }

      return m('.page.page-message.page-message-info',
        m('.container',
          m('.message-panel', [
            m('.message-icon',
              m('span.material-icon', 'info_outline')
            ),
            m('.message-body', [
              m('p.lead',
                gettext("Your account is inactive.")
              ),
              m('p',
                vm.activationMessage
              ),
              m('p', [
                activateButton,
                _.component('button', {
                  class: '.btn-default',
                  submit: false,
                  label: gettext("Request another link"),
                  onclick: form.reset.bind(form)
                })
              ])
            ])
          ])
        )
      );
    },
    form: function(form, _) {
      return m('.page.page-request-activation', [
        _.component('header', {
          title: gettext("Change forgotten password")
        }),
        m('.container',
          m('.row', [
            m('.col-md-8', [
              m('p',
                gettext("Because user passwords are processed in an irreversible way before being saved to database, it is not possible for us to simply send you your password.")
              ),
              m('p',
                gettext("Instead, you can change your password using special secure form that will be available by special link valid only for your browser, for seven days or until your password is changed.")
              ),
              m('p',
                gettext("To receive this link, enter your account's e-mail addres in form and press \"Send link\" button.")
              )
            ]),
            m('.col-md-4',
              _.component('request-link-form', form)
            )
          ])
        )
      ]);
    }
  };

  Misago.addService('route:request-password-change', function(_) {
    _.route('request-password-change', requestPasswordChange);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));
