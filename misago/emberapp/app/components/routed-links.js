import Ember from 'ember';

export default Ember.Component.extend({
  _clicksHandlerName: function() {
    return 'click.MisagoDelegatedLinks-' + this.get('elementId');
  }.property('elementId'),

  cleanHref: function(router, href) {
    if (!href) { return; }

    // Is link relative?
    var isRelative = href.substr(0, 1) === '/' && href.substr(0, 2) !== '//';

    // If link contains host, validate to see if its outgoing
    if (!isRelative) {
      var location = window.location;

      // If protocol matches current one, strip it from string
      // otherwhise stop handler
      if (href.substr(0, 2) !== '//') {
        var hrefProtocol = href.substr(0, location.protocol.length + 2);
        if (hrefProtocol !== location.protocol + '//') { return; }
        href = href.substr(location.protocol.length + 2);
      } else {
        href = href.substr(2);
      }

      // Host checks out?
      if (href.substr(0, location.host.length) !== location.host) { return; }
      href = href.substr(location.host.length);
    }

    // Is link within Ember app?
    var rootUrl = router.get('rootURL');
    if (href.substr(0, rootUrl.length) !== rootUrl) { return; }

    // Is link to media/static/avatar server?
    // NOTE: In ember serve staticUrl equals to /, making clean always fail
    var staticUrl = this.get('staticUrl');
    if (href.substr(0, staticUrl.length) === staticUrl) { return; }

    var mediaUrl = this.get('mediaUrl');
    if (href.substr(0, mediaUrl.length) === mediaUrl) { return; }

    var avatarsUrl = '/user-avatar/';
    if (href.substr(0, avatarsUrl.length) === avatarsUrl) { return; }

    return href;
  },

  delegateLinkClickHandler: function() {
    var self = this;
    var router = this.container.lookup('router:main');

    this.$().on(this.get('_clicksHandlerName'), 'a', function(e) {
      var cleanedHref = self.cleanHref(router, e.target.href);

      /*
      If href was cleaned, prevent default action on link
      and tell Ember's router to handle cleaned href instead.

      NOTE: there's no way to reliably decide if user didn't maliciously
      post an URL to something that should be routed by server instead, like
      admin control panel.

      If this happens, clicks on those links will fail in Ember's router,
      resulting in 404 page for valid urls, confusing your users.

      ...not like it's not your moderators job to keep an eye on what your
      users are posting on your own site.
      */
      if (cleanedHref) {
        e.preventDefault();
        router.handleURL(cleanedHref);
      }
    });
  }.on('didInsertElement'),

  removeLinkClickHandler: function() {
    this.$().off(this.get('_clicksHandlerName'));
  }.on('willDestroyElement')
});
