(function (Misago) {
  'use strict';

  var navbar = {
    style: '.nav.navbar-nav.navbar-compact-nav.hidden-md.hidden-lg',
    controller: function(links, _) {
      return {
        openUserMenu: function() {
          if (_.user.isAuthenticated) {
            _.dropdown.toggle('navbar-dropdown', 'navbar:dropdown:user');
          } else {
            _.dropdown.toggle('navbar-dropdown', 'navbar:dropdown:guest');
          }

          return false;
        }
      };
    },
    userMenu: function(ctrl, _) {
      if (_.user.isAuthenticated) {
        return {
          element: _.component('user-avatar', _.user, 64),
          config: {
            onclick: ctrl.openUserMenu,
            url: '/not-yet/',

            'data-misago-routed': 'false'
          }
        };
      } else {
        return {
          element: _.component('user-avatar', null, 64),
          config: {
            onclick: ctrl.openUserMenu,
            href: '#',

            'data-misago-routed': 'false'
          }
        };
      }
    },
    mobileNav: function(ctrl, links, _) {
      var mobileLinks = [
        {
          element: m('img', {
            src: _.router.staticUrl('misago/img/site-icon.png'),
            alt: _.settings.forum_name
          }),
          url: _.router.url('index')
        }
      ];

      links.forEach(function(link) {
        if (link.url !== mobileLinks[0].url) {
          mobileLinks.push(link);
        }
      });

      mobileLinks.push(this.userMenu(ctrl, _));

      return mobileLinks;
    },
    view: function(ctrl, links, _) {
      var mobileLinks = this.mobileNav(ctrl, links, _);

      return m('ul' + this.style + '.with-' + mobileLinks.length + '-items',
        mobileLinks.map(function(link) {
          return m('li',
            m('a', link.config || {href: link.url},
              link.element || m('span.material-icon', {title:link.label},
                link.icon
              )
            )
          );
        })
      );
    }
  };

  Misago.addService('component:navbar:mobile', function(_) {
    _.component('navbar:mobile', navbar);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
