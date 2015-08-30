(function (ns) {
  'use strict';

  var legalPageFactory = function(type_name, default_title) {
    var dashed_type_name = type_name.replace(/_/g, '-');

    var self = {
      is_destroyed: true,
      controller: function() {
        self.is_destroyed = false;
        self.vm.init();

        return {
          onunload: function() {
            self.is_destroyed = true;
          }
        };
      },
      vm: {
        is_busy: false,
        is_ready: false,
        content: null,

        init: function() {
          var _ = self.container;

          var vm = this;
          if (vm.is_ready) {
            _.setTitle(vm.title);
          } else {
            _.setTitle();

            if (!vm.is_busy) {
              vm.is_busy = true;

              _.api.one('legal-pages', dashed_type_name).then(function(data) {
                vm.title = data.title || default_title;
                vm.body = data.body;
                vm.is_busy = false;
                vm.is_ready = true;

                if (!self.is_destroyed) {
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

        if (this.vm.is_ready) {
          return m('.page.page-legal.page-legal-' + dashed_type_name, [
            _.component(ns.PageHeader, {title: this.vm.title}),
            m('.container',
              m.trust(this.vm.body)
            )
          ]);
        } else {
          return _.component(ns.LoadingPage);
        }
      }
    };
    return self;
  };

  ns.TermsOfServicePage = legalPageFactory(
    'terms_of_service', gettext('Terms of service'));
  ns.PrivacyPolicyPage = legalPageFactory(
    'privacy_policy', gettext('Privacy policy'));
}(Misago.prototype));
