(function (Misago) {
  'use strict';

  var index = {
    controller: function() {
      var _ = this.container;
      document.title = _.settings.forum_index_title || _.settings.forum_name;

      var count = m.prop(0);

      return {
        count: count,
        increment: function() {
          console.log('increment()');
          count(count() + 1);
        }
      };
    },
    view: function(ctrl) {
      return m('.container', [
        m('h1', [
          'Count: ', m('strong', ctrl.count())
        ]),
        m('p', 'Clicky click button to increase count!.'),
        m('p',
          m('button.btn.btn-primary', {onclick: ctrl.increment},
            'Clicky clicky!'
          )
        )
      ]);
    }
  };

  Misago.addService('route:index', {
    factory: function(_) {
      _.route('index', index);
    },
    after: 'routes'
  });
}(Misago.prototype));
