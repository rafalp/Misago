(function (ns) {
  'use strict';

  var legalLink = function(_, legal_type, default_title) {
    var url = ns.get(_.settings, legal_type + '_link');
    if (!url && ns.get(_.settings, legal_type)) {
      url = _.router.url(legal_type);
    }

    if (url) {
      return m('li',
        m('a', {href: url}, ns.get(_.settings, legal_type + '_title', default_title))
      );
    } else {
      return null;
    }
  };

  ns.FooterNav = {
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

      items.push(legalLink(_, 'terms_of_service', gettext('Terms of service')));
      items.push(legalLink(_, 'privacy_policy', gettext('Privacy policy')));

      return m('ul.list-inline.footer-nav', items);
    }
  };
}(Misago.prototype));
