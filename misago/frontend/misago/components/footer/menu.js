(function (Misago) {
  'use strict';

  var legalLink = function(_, legalType, defaultTitle) {
    var url = Misago.get(_.settings, legalType + '_link');
    if (!url && Misago.get(_.settings, legalType)) {
      url = _.router.url(legalType);
    }

    if (url) {
      return m('li',
        m('a', {href: url},
          Misago.get(_.settings, legalType + '_title', defaultTitle)
        )
      );
    } else {
      return null;
    }
  };

  var menu = {
    isVisible: function(settings) {
      return [
        !!settings.forum_footnote,
        !!settings.terms_of_service,
        !!settings.terms_of_service_link,
        !!settings.privacy_policy,
        !!settings.privacy_policy_link
      ].indexOf(true) !== -1;
    },
    view: function(ctrl, _) {
      var items = [];

      if (_.settings.forum_footnote) {
        items.push(m('li.forum-footnote', m.trust(_.settings.forum_footnote)));
      }

      items.push(
        legalLink(_, 'terms_of_service', gettext('Terms of service')));
      items.push(
        legalLink(_, 'privacy_policy', gettext('Privacy policy')));

      return m('ul.list-inline.footer-nav', items);
    }
  };

  Misago.addService('component:footer:menu', {
    factory: function(_) {
      _.component('footer:menu', menu);
    },
    after: 'components'
  });
}(Misago.prototype));
