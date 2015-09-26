(function (Misago) {
  'use strict';

  var legalPageFactory = function(typeName, defaultTitle) {
    var dashedTypeName = typeName.replace(/_/g, '-');

    return Misago.route({
      controller: function() {
        var _ = this.container;

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

          page.title = page.title || defaultTitle;
          this.page = page;
          this.isReady = true;

          m.endComputation();

          if (component.isActive) {
            _.title.set(this.page.title);
          }
        }
      },
      view: function() {
        var _ = this.container;

        return m('.page.legal-page.' + dashedTypeName + '-page', [
          _.component(Misago.PageHeader, {title: this.vm.page.title}),
          m('.container',
            _.component(Misago.Markup, this.vm.page.body)
          )
        ]);
      }
    });
  };

  Misago.TermsOfServiceRoute = legalPageFactory(
    'terms_of_service', gettext('Terms of service'));
  Misago.PrivacyPolicyRoute = legalPageFactory(
    'privacy_policy', gettext('Privacy policy'));
}(Misago.prototype));
