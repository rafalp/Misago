import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('controller:footer', 'FooterController');

test('it exists', function() {
  var controller = this.subject();
  ok(controller);
});

test('showTermsLink', function() {
  var controller = this.subject();

  // ToS isn't defined and there isn't link to remote ToS page, don't show link
  controller.set('settings', {'terms_of_service': null, 'terms_of_service_link': ''});
  ok(!controller.get('showTermsLink'));

  // ToS is defined but there isn't link to remote ToS page, show link
  controller.set('settings', {'terms_of_service': true, 'terms_of_service_link': ''});
  ok(controller.get('showTermsLink'));

  // ToS isn't defined but there is link to remote ToS page, show link
  controller.set('settings', {'terms_of_service': null, 'terms_of_service_link': 'http://somewhere.com'});
  ok(controller.get('showTermsLink'));

  // ToS is defined and there is link to remote ToS page, show link
  controller.set('settings', {'terms_of_service': true, 'terms_of_service_link': 'http://somewhere.com'});
  ok(controller.get('showTermsLink'));
});

test('showPrivacyLink', function() {
  var controller = this.subject();

  // PrivPolicy isn't defined and there isn't link to remote PrivPolicy page, don't show link
  controller.set('settings', {'privacy_policy': null, 'privacy_policy_link': ''});
  ok(!controller.get('showPrivacyLink'));

  // PrivPolicy is defined but there isn't link to remote PrivPolicy page, show link
  controller.set('settings', {'privacy_policy': true, 'privacy_policy_link': ''});
  ok(controller.get('showPrivacyLink'));

  // PrivPolicy isn't defined but there is link to remote PrivPolicy page, show link
  controller.set('settings', {'privacy_policy': null, 'privacy_policy_link': 'http://somewhere.com'});
  ok(controller.get('showPrivacyLink'));

  // PrivPolicy is defined and there is link to remote PrivPolicy page, show link
  controller.set('settings', {'privacy_policy': true, 'privacy_policy_link': 'http://somewhere.com'});
  ok(controller.get('showPrivacyLink'));
});

test('showNav', function() {
  var controller = this.subject();

  // no Privacy Policy or ToS, don't show footer nav
  controller.set('settings', {
    'terms_of_service': null, 'terms_of_service_link': '',
    'privacy_policy': null, 'privacy_policy_link': ''
  });
  ok(!controller.get('showNav'));

  // Privacy Policy but no ToS, don't show footer nav
  controller.set('settings', {
    'terms_of_service': null, 'terms_of_service_link': '',
    'privacy_policy': true, 'privacy_policy_link': ''
  });
  ok(controller.get('showNav'));

  // no Privacy Policy but ToS, don't show footer nav
  controller.set('settings', {
    'terms_of_service': null, 'terms_of_service_link': 'http://somewhere.com',
    'privacy_policy': null, 'privacy_policy_link': ''
  });
  ok(controller.get('showNav'));

  // Privacy Policy and ToS, don't show footer nav
  controller.set('settings', {
    'terms_of_service': null, 'terms_of_service_link': 'http://somewhere.com',
    'privacy_policy': null, 'privacy_policy_link': 'http://somewhere.com'
  });
  ok(controller.get('showNav'));
});
