(function (Misago) {
  'use strict';

  var formOptions = {
    endpoint: 'send-activation',
    user: null,

    success: function(user) {
      this.user = user;
    },
    error: function(rejection, _) {
      if (rejection.code === 'already_active') {
        _.alert.info(rejection.detail);
        _.modal('sign-in');
      } else if (rejection.code === 'inactive_admin') {
        _.alert.info(rejection.detail);
      } else {
        _.alert.error(rejection.detail);
      }
    },
    reset: function() {
      this.user = null;
    }
  };

  var requestActivation = {
    controller: function(_) {
      _.auth.denyAuthenticated(
        gettext("You have to be signed out to activate account."));

      _.title.set(gettext("Activate your account"));

      return {
        form: _.form('request-link', formOptions)
      };
    },
    view: function(ctrl, _) {
      if (formOptions.user) {
        return this.completed(ctrl.form, formOptions, _);
      } else {
        return this.form(ctrl.form, _);
      }
    },
    completed: function(form, formOptions, _) {
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
                  username: formOptions.user.username,
                  email: formOptions.user.email
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
