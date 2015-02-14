import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('controller:flash-message', 'FlashMessageController');

test('it exists', function(assert) {
  var controller = this.subject();
  assert.ok(controller);
});

test('isInfo', function(assert) {
  var controller = this.subject();

  controller.set('type', 'info');

  assert.ok(controller.get('isInfo'));
  assert.ok(!controller.get('isSuccess'));
  assert.ok(!controller.get('isWarning'));
  assert.ok(!controller.get('isError'));
});

test('isSuccess', function(assert) {
  var controller = this.subject();

  controller.set('type', 'success');

  assert.ok(!controller.get('isInfo'));
  assert.ok(controller.get('isSuccess'));
  assert.ok(!controller.get('isWarning'));
  assert.ok(!controller.get('isError'));
});

test('isWarning', function(assert) {
  var controller = this.subject();

  controller.set('type', 'warning');

  assert.ok(!controller.get('isInfo'));
  assert.ok(!controller.get('isSuccess'));
  assert.ok(controller.get('isWarning'));
  assert.ok(!controller.get('isError'));
});

test('isError', function(assert) {
  var controller = this.subject();

  controller.set('type', 'error');

  assert.ok(!controller.get('isInfo'));
  assert.ok(!controller.get('isSuccess'));
  assert.ok(!controller.get('isWarning'));
  assert.ok(controller.get('isError'));
});

test('setFlash', function(assert) {
  var controller = this.subject();

  var testMessage = "I'm test flash!";

  controller.send('setFlash', 'success', testMessage);

  assert.ok(controller.get('isVisible'));
  assert.ok(controller.get('isSuccess'));
  assert.equal(controller.get('message'), testMessage);
});

test('showFlash', function(assert) {
  var controller = this.subject();

  var testMessage = "I'm test flash!";

  controller.showFlash('success', testMessage);

  assert.ok(controller.get('isVisible'));
  assert.ok(controller.get('isSuccess'));
  assert.equal(controller.get('message'), testMessage);
});
