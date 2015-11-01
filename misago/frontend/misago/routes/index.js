(function (Misago) {
  'use strict';

  var index = {
    controller: function(_) {
      document.title = _.settings.forum_index_title || _.settings.forum_name;

      return {
        activation: function() {
          _.router.url('request_activation');
        }
      };
    },
    view: function(ctrl, _) {
      return m('.container', [
        m('h1', 'Activation'),
        m('p', 'Test auth blocks'),
        m('p',
          m('a', {href: _.router.url('request_activation')},
            'Request activation.'
          )
        )
      ]);
    }
  };

  Misago.addService('route:index', function(_) {
    _.route('index', index);
  },
  {
    after: 'routes'
  });
}(Misago.prototype));
