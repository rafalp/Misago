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
    view: function(ctrl, _) {
      var styles = [
        'default', 'primary', 'success',
        'info', 'warning', 'danger'
      ];

      return m('.container', [
        m('h1', 'Buttons'),
        m('', styles.map(function(item) {
          return m('', [
            _.component('button', {
              class: '.btn-' + item,
              label: 'Lorem ipsum'
            }),
            _.component('button', {
              class: '.btn-' + item,
              label: 'Lorem ipsum',
              loading: true
            })
          ]);
        }))
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
