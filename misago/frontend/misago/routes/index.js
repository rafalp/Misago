(function (Misago) {
  'use strict';

  var index = {
    controller: function(_) {
      document.title = _.settings.forum_index_title || _.settings.forum_name;

      return {
        active: function() {
          _.modal('register-complete', {
            'activation': 'active',
            'username': 'BobBoberson',
            'email': 'bob-boberson@somewhere.com'
          });
        },
        user: function() {
          _.modal('register-complete', {
            'activation': 'by_user',
            'username': 'BobBoberson',
            'email': 'bob-boberson@somewhere.com'
          });
        },
        admin: function() {
          _.modal('register-complete', {
            'activation': 'by_admin',
            'username': 'BobBoberson',
            'email': 'bob-boberson@somewhere.com'
          });
        }
      };
    },
    view: function(ctrl, _) {
      return m('.container', [
        m('h1', 'Buttons'),
        m('p', 'Test registration successful modal!'),
        m('',
          _.component('button', {
            class: '.btn-success',
            label: 'Registration done, account active',
            onclick: ctrl.active
          })
        ),
        m('',
          _.component('button', {
            class: '.btn-warning',
            label: 'Registration done, account inactive (user)',
            onclick: ctrl.user
          })
        ),
        m('',
          _.component('button', {
            class: '.btn-danger',
            label: 'Registration done, account inactive (admin)',
            onclick: ctrl.admin
          })
        ),
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
