import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('component:forum-footer', 'FooterComponent');

test('it exists', function(assert) {
  var component = this.subject();
  assert.ok(component);
});

test('showTermsLink', function(assert) {
  assert.expect(4);

  var component = this.subject();

  // ToS isn't defined and there isn't link to remote ToS page, don't show link
  component.set('settings', {'terms_of_service': null, 'terms_of_service_link': ''});
  assert.ok(!component.get('showTermsLink'));

  // ToS is defined but there isn't link to remote ToS page, show link
  component.set('settings', {'terms_of_service': true, 'terms_of_service_link': ''});
  assert.ok(component.get('showTermsLink'));

  // ToS isn't defined but there is link to remote ToS page, show link
  component.set('settings', {'terms_of_service': null, 'terms_of_service_link': 'http://somewhere.com'});
  assert.ok(component.get('showTermsLink'));

  // ToS is defined and there is link to remote ToS page, show link
  component.set('settings', {'terms_of_service': true, 'terms_of_service_link': 'http://somewhere.com'});
  assert.ok(component.get('showTermsLink'));
});

test('showPrivacyLink', function(assert) {
  assert.expect(4);

  var component = this.subject();

  // PrivPolicy isn't defined and there isn't link to remote PrivPolicy page, don't show link
  component.set('settings', {'privacy_policy': null, 'privacy_policy_link': ''});
  assert.ok(!component.get('showPrivacyLink'));

  // PrivPolicy is defined but there isn't link to remote PrivPolicy page, show link
  component.set('settings', {'privacy_policy': true, 'privacy_policy_link': ''});
  assert.ok(component.get('showPrivacyLink'));

  // PrivPolicy isn't defined but there is link to remote PrivPolicy page, show link
  component.set('settings', {'privacy_policy': null, 'privacy_policy_link': 'http://somewhere.com'});
  assert.ok(component.get('showPrivacyLink'));

  // PrivPolicy is defined and there is link to remote PrivPolicy page, show link
  component.set('settings', {'privacy_policy': true, 'privacy_policy_link': 'http://somewhere.com'});
  assert.ok(component.get('showPrivacyLink'));
});

test('hasContent', function(assert) {
  assert.expect(4);

  var component = this.subject();

  // no Privacy Policy or ToS, don't show footer nav
  component.set('settings', {
    'terms_of_service': null, 'terms_of_service_link': '',
    'privacy_policy': null, 'privacy_policy_link': ''
  });
  assert.ok(!component.get('hasContent'));

  // Privacy Policy but no ToS, don't show footer nav
  component.set('settings', {
    'terms_of_service': null, 'terms_of_service_link': '',
    'privacy_policy': true, 'privacy_policy_link': ''
  });
  assert.ok(component.get('hasContent'));

  // no Privacy Policy but ToS, don't show footer nav
  component.set('settings', {
    'terms_of_service': null, 'terms_of_service_link': 'http://somewhere.com',
    'privacy_policy': null, 'privacy_policy_link': ''
  });
  assert.ok(component.get('hasContent'));

  // Privacy Policy and ToS, don't show footer nav
  component.set('settings', {
    'terms_of_service': null, 'terms_of_service_link': 'http://somewhere.com',
    'privacy_policy': null, 'privacy_policy_link': 'http://somewhere.com'
  });
  assert.ok(component.get('hasContent'));
});
