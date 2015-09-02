(function (Misago) {
  'use strict';

  var legalPageFactory = function(typeName, defaultTitle) {
    var dashedTypeName = typeName.replace(/_/g, '-');

    var self = {
      isDestroyed: true,
      controller: function() {
        var _ = self.container;
        self.isDestroyed = false;

        if (Misago.get(_.settings, typeName + '_link')) {
          window.location = Misago.get(_.settings, typeName + '_link');
        } else {
          self.vm.init(_);
        }

        return {
          onunload: function() {
            self.isDestroyed = true;
          }
        };
      },
      vm: {
        isBusy: false,
        isReady: false,
        content: null,

        init: function(_) {

          var vm = this;
          if (vm.isReady) {
            _.setTitle(vm.title);
          } else {
            _.setTitle();

            if (!vm.isBusy) {
              vm.isBusy = true;

              _.api.one('legal-pages', dashedTypeName).then(function(data) {
                vm.title = data.title || defaultTitle;
                vm.body = data.body;
                vm.isBusy = false;
                vm.isReady = true;

                if (!self.isDestroyed) {
                  _.setTitle(vm.title);
                  m.redraw();
                }
              });
            }
          }
        }
      },
      view: function() {
        var _ = this.container;

        if (this.vm.isReady) {
          return m('.page.page-legal.page-legal-' + dashedTypeName, [
            _.component(Misago.PageHeader, {title: this.vm.title}),
            m('.container',
              m.trust(this.vm.body)
            )
          ]);
        } else {
          return _.component(Misago.LoadingPage);
        }
      }
    };
    return self;
  };

  Misago.TermsOfServicePage = legalPageFactory(
    'terms_of_service', gettext('Terms of service'));
  Misago.PrivacyPolicyPage = legalPageFactory(
    'privacy_policy', gettext('Privacy policy'));
}(Misago.prototype));
