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

  Misago.Error403Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Page not available'));
    },
    error: null,
    view: function() {
      return m('.page.error-page.error-403-page',
        m('.container', [
          m('h1', 'Error 403!'),
          m('p.lead', this.error || 'No perm to see this page')
        ])
      );
    }
  });

  Misago.Error404Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Page not found'));
    },
    view: function() {
      return errorPage({
        code: 404,
        icon: 'gesture',
        message: gettext("Requested page could not be found."),
        help: gettext("The link you clicked was incorrect or the page has been moved or deleted.")
      });
    }
  });

  Misago.Error500Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Application error occured'));
    },
    view: function() {
      return errorPage({
        code: 500,
        icon: 'error_outline',
        message: gettext("Requested page could not be displayed due to an error.")
      });
    }
  });

  Misago.Error0Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Lost connection to application'));
    },
    view: function() {
      return errorPage({
        code: 500,
        icon: 'sync_problem',
        message: gettext("Could not connect to application."),
        help: gettext("This may be caused by problems with your connection or application server. Please check your inter connection and refresh page if problem persists.")
      });
    }
  });
}(Misago.prototype));
