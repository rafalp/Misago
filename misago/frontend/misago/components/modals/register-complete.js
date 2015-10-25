(function (Misago) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var refresh = function() {
    document.location.reload();
  };

  var registerComplete = {
    controller: function(message, _) {
      if (message.activation === 'active') {
        _.runloop.runOnce(
          refresh, 'refresh-after-registration', 10000);
      }
    },
    view: function(ctrl, message, _) {
      var messageHtml = null;

      if (message.activation === 'active') {
        messageHtml = this.active(message);
      } else {
        messageHtml = this.inactive(message);
      }

      return m('.modal-dialog.modal-message.modal-register[role="document"]',
        {config: persistent},
        m('.modal-content', [
          _.component('modal:header', gettext('Registration complete')),
          m('.modal-body',
            messageHtml
          )
        ])
      );
    },
    active: function(message) {
      var lead = gettext("%(username)s, your account has been created and you were signed in.");
      return [
        m('.message-icon',
          m('span.material-icon', 'check')
        ),
        m('.message-body', [
          m('p.lead',
            interpolate(lead, {'username': message.username}, true)
          ),
          m('p',
            gettext('The page will refresh automatically in 10 seconds.')
          ),
          m('p',
            m('button[type="button"].btn.btn-default', {onclick: refresh},
              gettext('Refresh page')
            )
          )
        ])
      ];
    },
    inactive: function(message) {
      var lead = null;
      var help = null;

      if (message.activation === 'user') {
        lead = gettext("%(username)s, your account has been created but you need to activate it before you will be able to sign in.");
        help = gettext("We have sent an e-mail to %(email)s with link that you have to click to activate your account.");
      } else if (message.activation === 'admin') {
        lead = gettext("%(username)s, your account has been created but board administrator will have to activate it before you will be able to sign in.");
        help = gettext("We will send an e-mail to %(email)s when this takes place.");
      }

      return [
        m('.message-icon',
          m('span.material-icon', 'info_outline')
        ),
        m('.message-body', [
          m('p.lead',
            interpolate(lead, {'username': message.username}, true)
          ),
          m('p',
            interpolate(help, {'email': message.email}, true)
          )
        ])
      ];
    }
  };

  Misago.addService('modal:register-complete', function(_) {
    _.modal('register-complete', registerComplete);
  },
  {
    after: 'modals'
  });
}(Misago.prototype));
