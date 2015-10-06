(function (Misago) {
  'use strict';

  var legalPageFactory = function(typeName, defaultTitle) {
    var dashedTypeName = typeName.replace(/_/g, '-');

    return {
      controller: function(_) {
        if (Misago.get(_.settings, typeName + '_link')) {
          window.location = Misago.get(_.settings, typeName + '_link');
        } else {
          this.vm.init(this, _);
        }
      },
      vm: {
        page: null,
        isReady: false,
        init: function(component, _) {
          if (this.isReady) {
            _.title.set(this.title);
          } else {
            _.title.set();
            return _.api.model('legal-page', dashedTypeName);
          }
        },
        ondata: function(page, component, _) {
          m.startComputation();

          if (page.link) {
            window.location = page.link;
          } else {
            page.title = page.title || defaultTitle;
            this.page = page;
            this.isReady = true;

            m.endComputation();

            if (component.isActive) {
              _.title.set(this.page.title);
            }
          }
        }
      },
      view: function(ctrl, _) {
        return m('.page.legal-page.' + dashedTypeName + '-page', [
          _.component('header', {title: this.vm.page.title}),
          m('.container',
            _.component('markup', this.vm.page.body)
          )
        ]);
      }
    };
  };

  Misago.addService('route:legal-pages', {
    factory: function(_) {
      _.route('terms-of-service', legalPageFactory(
        'terms_of_service', gettext('Terms of service')));
      _.route('privacy-policy', legalPageFactory(
        'privacy_policy', gettext('Privacy policy')));
    },
    after: 'routes'
  });
}(Misago.prototype));
