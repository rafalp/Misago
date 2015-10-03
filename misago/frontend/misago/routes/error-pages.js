(function (Misago) {
  'use strict';

  var errorPage = function(error) {
    var error_message = [
      m('p.lead', error.message)
    ];

    if (error.help) {
      error_message.push(m('p.help', error.help));
    }

    return m('.page.error-page.error-' + error.code + '-page',
      m('.container',
        m('.error-panel', [
          m('.error-icon',
            m('span.material-icon', error.icon)
          ),
          m('.error-message', error_message)
        ])
      )
    );
  };

  var errorBanned = {
    controller: function() {
      this.container.title.set(gettext('You are banned'));
    },
    error: null,
    view: function() {
      var error_message = [];
      if (this.error.ban.message.html) {
        error_message.push(m('.lead', m.trust(this.error.ban.message.html)));
      } else {
        error_message.push(m('p.lead', this.error.message));
      }

      var expirationMessage = null;
      if (this.error.ban.expires_on) {
        if (this.error.ban.expires_on.isAfter(moment())) {
          expirationMessage = interpolate(
            gettext('This ban expires %(expires_on)s.'),
            { 'expires_on': this.error.ban.expires_on.fromNow() },
            true);
        } else {
          expirationMessage = gettext('This ban has expired.');
        }
      } else {
        expirationMessage = gettext('This ban is permanent.');
      }
      error_message.push(m('p', expirationMessage));

      return m('.page.error-page.error-banned-page',
        m('.container',
          m('.error-panel', [
            m('.error-icon',
              m('span.material-icon', 'highlight_off')
            ),
            m('.error-message', error_message)
          ])
        )
      );
    }
  };

  var error403 = {
    controller: function() {
      this.container.title.set(gettext('Page not available'));
    },
    error: null,
    view: function() {
      if (this.error === "Permission denied") {
        this.error = gettext("You don't have permission to access this page.");
      }

      return errorPage({
        code: 403,
        icon: 'remove_circle_outline',
        message: gettext("This page is not available."),
        help: this.error
      });
    }
  };

  var error404 = {
    controller: function() {
      this.container.title.set(gettext('Page not found'));
    },
    view: function() {
      return errorPage({
        code: 404,
        icon: 'info_outline',
        message: gettext("Requested page could not be found."),
        help: gettext("The link you followed was incorrect or the page has been moved or deleted.")
      });
    }
  };

  var error500 = {
    controller: function() {
      this.container.title.set(gettext('Application error occured'));
    },
    view: function() {
      return errorPage({
        code: 500,
        icon: 'error_outline',
        message: gettext("Requested page could not be displayed due to an error."),
        help: gettext("Please try again later or contact site staff if error persists.")
      });
    }
  };

  var error0 = {
    controller: function() {
      this.container.title.set(gettext('Lost connection with application'));
    },
    view: function() {
      return errorPage({
        code: 0,
        icon: 'sync_problem',
        message: gettext("Could not connect to application."),
        help: gettext("This may be caused by problems with your connection or application server. Please check your internet connection and refresh page if problem persists.")
      });
    }
  };

  Misago.addService('route:error-pages', {
    factory: function(_) {
      _.route('error:banned', errorBanned);
      _.route('error:403', error403);
      _.route('error:404', error404);
      _.route('error:500', error500);
      _.route('error:0', error0);
    },
    after: 'routes'
  });
}(Misago.prototype));
