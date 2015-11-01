(function (Misago) {
  'use strict';

  var viewModel = {
    error: null,
    isReady: false,

    form: null,

    init: function(_) {
      this.error = null;
      this.user = null;
      this.isReady = false;

      var endpoint = _.api.endpoint('auth').endpoint('change-password');
      endpoint = endpoint.endpoint(m.route.param('user_id'));
      endpoint = endpoint.endpoint(m.route.param('token'));

      return endpoint.get();
    },
    ondata: function(data, _) {
      m.startComputation();

      _.title.set(gettext("Change forgotten password"));

      this.form = _.form('change-password');
      this.isReady = true;

      m.endComputation();
    },
    onerror: function(error, _) {
      if (error.status === 400) {
        m.startComputation();

        this.error = error;
        this.isReady = true;

        m.endComputation();
      } else {
        _.router.errorPage(error);
      }
    }
  };

  var changePassword = {
    controller: function(_) {
      this.vm.init(_);

      return {
        signin: function() {
          _.modal('sign-in');
        }
      };
    },
    vm: viewModel,
    view: function(ctrl, _) {
      if (this.vm.error) {
        return this.rejected(this.vm.error, _);
      } else {
        if (this.vm.form.username) {
          return this.complete(ctrl, this.vm.form.username, _);
        } else {
          return this.form(this.vm.form, _);
        }
      }
    },
    form: function(form, _) {
      return m('.page.page-change-password', [
        _.component('header', {
          title: gettext("Change forgotten password")
        }),
        m('.container',
          m('.row',
            m('.col-md-4.col-md-offset-4',
              m('.well.well-form',
                m('form', {onsubmit: form.submit}, [
                  m('.form-group',
                    m('.control-input',
                      Misago.input({
                        disabled: form.isBusy,
                        value: form.password,
                        type: 'password',
                        placeholder: gettext("Enter new password")
                      })
                    )
                  ),
                  _.component('button', {
                    class: '.btn-primary.btn-block',
                    submit: true,
                    loading: form.isBusy,
                    label: gettext("Change password")
                  })
                ])
              )
            )
          )
        )
      ]);
    },
    complete: function(ctrl, username, _) {
      var message = gettext("%(username)s, your password has been changed successfully.");

      return m('.page.page-message.page-message-success',
        m('.container',
          m('.message-panel', [
            m('.message-icon',
              m('span.material-icon', 'check')
            ),
            m('.message-body', [
              m('p.lead',
                interpolate(message, {
                  username: username
                }, true)
              ),
              m('p',
                gettext("You can now sign in to your account using your new password.")
              ),
              m('p',
                _.component('button', {
                  class: '.btn-default',
                  submit: false,
                  label: gettext("Sign in"),
                  onclick: ctrl.signin
                })
              )
            ])
          ])
        )
      );
    },
    rejected: function(error) {
      return m('.page.page-message.page-message-info',
        m('.container',
          m('.message-panel', [
            m('.message-icon',
              m('span.material-icon', 'info_outline')
            ),
            m('.message-body', [
              m('p.lead',
                gettext("Your account can't be activated at this time.")
              ),
              m('p',
                error.detail
              )
            ])
          ])
        )
      );
    }
  };

  Misago.addService('route:change-password', function(_) {
    _.route('change-password', changePassword);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));
