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
        isReady: false,
        init: function(component, _) {
          if (this.isReady) {
            _.title.set(this.title);
          } else {
            _.title.set();
            return _.api.one('legal-pages', dashedTypeName);
          }
        },
        ondata: function(data, component, _) {
          m.startComputation();

          this.title = data.title || defaultTitle;
          this.body = data.body;
          this.isReady = true;

          m.endComputation();

          if (component.isActive) {
            _.title.set(data.title);
          }
        }
      },
      view: function() {
        var _ = this.container;

        return m('.page.legal-page.' + dashedTypeName + '-page', [
          _.component(Misago.PageHeader, {title: this.vm.title}),
          m('.container',
            m.trust(this.vm.body)
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
