(function (Misago) {
  'use strict';

  Misago.Error403Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Page not available'));
    },
    error: null,
    view: function(ctrl) {
      return m('.container', [
        m('h1', 'Error 403!'),
        m('p.lead', this.error || 'No perm to see this page')
      ]);
    }
  });

  Misago.Error404Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Page not found'));
    },
    view: function(ctrl) {
      return m('.container', [
        m('h1', 'Error 404!'),
        m('p.lead', 'Requested page could not be found.')
      ]);
    }
  });

  Misago.Error500Route = Misago.route({
    controller: function() {
      this.container.setTitle(gettext('Application error occured'));
    },
    view: function(ctrl) {
      return m('.container', [
        m('h1', 'Error 500!'),
        m('p.lead', 'Application has derped.')
      ]);
    }
  });
}(Misago.prototype));
