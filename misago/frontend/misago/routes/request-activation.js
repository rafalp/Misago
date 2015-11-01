(function (Misago) {
  'use strict';

  var ViewModel = function() {
    this.endpoint = 'send-activation';
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

  var requestActivation = {
    controller: function(_) {
      _.auth.denyAuthenticated(
        gettext("You have to be signed out to activate account."));

      _.title.set(gettext("Activate your account"));

      var vm = new ViewModel();

      return {
        vm: vm,
        form: _.form('request-link', vm)
      };
    },
    view: function(ctrl, _) {
      if (ctrl.vm.user) {
        return this.completed(ctrl.form, ctrl.vm, _);
      } else {
        return this.form(ctrl.form, _);
      }
    },
    completed: function(form, vm, _) {
      var message = gettext("%(username)s, we have sent your activation link to %(email)s.");

      return m('.page.page-message.page-message-success',
        m('.container',
          m('.message-panel', [
            m('.message-icon',
              m('span.material-icon', 'check')
            ),
            m('.message-body', [
              m('p.lead',
                gettext("Activation link has been sent.")
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
    form: function(form, _) {
      return m('.page.page-request-activation', [
        _.component('header', {
          title: gettext("Request activation link")
        }),
        m('.container',
          m('.row', [
            m('.col-md-8', [
              m('p',
                gettext("Site administrator may impose requirement on newly regitered accounts to be activated before users will be able to sign in.")
              ),
              m('p',
                gettext("Depending on time of registration, you will be able activate your account by clicking special activation link. This link will be valid only for your browser, for seven days or until your account is activated.")
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

  Misago.addService('route:request-activation', function(_) {
    _.route('request-activation', requestActivation);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));
