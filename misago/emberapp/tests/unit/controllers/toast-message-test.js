import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('service:toast-message', 'ToastMessageService');

test('it exists', function(assert) {
  var service = this.subject();
  assert.ok(service);
});

test('isInfo', function(assert) {
  var service = this.subject();

  service.set('type', 'info');

  assert.ok(service.get('isInfo'));
  assert.ok(!service.get('isSuccess'));
  assert.ok(!service.get('isWarning'));
  assert.ok(!service.get('isError'));
});

test('isSuccess', function(assert) {
  var service = this.subject();

  service.set('type', 'success');

  assert.ok(!service.get('isInfo'));
  assert.ok(service.get('isSuccess'));
  assert.ok(!service.get('isWarning'));
  assert.ok(!service.get('isError'));
});

test('isWarning', function(assert) {
  var service = this.subject();

  service.set('type', 'warning');

  assert.ok(!service.get('isInfo'));
  assert.ok(!service.get('isSuccess'));
  assert.ok(service.get('isWarning'));
  assert.ok(!service.get('isError'));
});

test('isError', function(assert) {
  var service = this.subject();

  service.set('type', 'error');

  assert.ok(!service.get('isInfo'));
  assert.ok(!service.get('isSuccess'));
  assert.ok(!service.get('isWarning'));
  assert.ok(service.get('isError'));
});

test('_setToast', function(assert) {
  var service = this.subject();

  var testMessage = "I'm test toast!";

  service._setToast('success', testMessage);

  assert.ok(service.get('isVisible'));
  assert.ok(service.get('isSuccess'));
  assert.equal(service.get('message'), testMessage);
});

test('_showToast', function(assert) {
  var service = this.subject();

  var testMessage = "I'm test toast!";

  service._showToast('success', testMessage);

  assert.ok(service.get('isVisible'));
  assert.ok(service.get('isSuccess'));
  assert.equal(service.get('message'), testMessage);
});
