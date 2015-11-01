(function (Misago) {
  'use strict';

  var viewModel = {
    error: null,
    username: null,
    isReady: false,
    init: function(_) {
      this.error = null;
      this.user = null;
      this.isReady = false;

      var endpoint = _.api.endpoint('auth').endpoint('activate-account');
      endpoint = endpoint.endpoint(m.route.param('user_id'));
      endpoint = endpoint.endpoint(m.route.param('token'));

      return endpoint.post();
    },
    ondata: function(data, _) {
      m.startComputation();

      _.title.set(gettext("Account activated"));

      this.username = data.username;
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

  var activateByToken = {
    controller: function(_) {
      _.auth.denyAuthenticated(
        gettext("You have to be signed out to activate account."));

      _.title.set(gettext("Account activation"));
      this.vm.init(_);
    },
    vm: viewModel,
    view: function(ctrl, _) {
      if (this.vm.error) {
        return this.rejected(this.vm.error, _);
      } else {
        return this.success(this.vm.username, _);
      }
    },
    success: function(username) {
      var message = gettext("%(username)s, your account has been successfully activated!");

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
                gettext('You can now sign in to finish setting up your account and to participate in or start new discussions.')
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
    },
    loading: function(ctrl, _) {
      return m('.page.page-loading', [
        _.component('loader'),
        m('p.lead', gettext("Activating account..."))
      ]);
    }
  };

  Misago.addService('route:activate-by-token', function(_) {
    _.route('activate-by-token', activateByToken);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));
