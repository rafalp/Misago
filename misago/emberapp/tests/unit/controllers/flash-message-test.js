import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('controller:flash-message', 'FlashMessageController');

test('it exists', function() {
  var controller = this.subject();
  ok(controller);
});

test('isInfo', function() {
  var controller = this.subject();

  controller.set('type', 'info');

  ok(controller.get('isInfo'));
  ok(!controller.get('isSuccess'));
  ok(!controller.get('isWarning'));
  ok(!controller.get('isError'));
});

test('isSuccess', function() {
  var controller = this.subject();

  controller.set('type', 'success');

  ok(!controller.get('isInfo'));
  ok(controller.get('isSuccess'));
  ok(!controller.get('isWarning'));
  ok(!controller.get('isError'));
});

test('isWarning', function() {
  var controller = this.subject();

  controller.set('type', 'warning');

  ok(!controller.get('isInfo'));
  ok(!controller.get('isSuccess'));
  ok(controller.get('isWarning'));
  ok(!controller.get('isError'));
});

test('isError', function() {
  var controller = this.subject();

  controller.set('type', 'error');

  ok(!controller.get('isInfo'));
  ok(!controller.get('isSuccess'));
  ok(!controller.get('isWarning'));
  ok(controller.get('isError'));
});

test('setFlash', function() {
  var controller = this.subject();

  var testMessage = "I'm test flash!";

  controller.send('setFlash', 'success', testMessage);

  ok(controller.get('isVisible'));
  ok(controller.get('isSuccess'));
  equal(controller.get('message'), testMessage);
});

test('showFlash', function() {
  var controller = this.subject();

  var testMessage = "I'm test flash!";

  controller.send('showFlash', 'success', testMessage);

  ok(controller.get('isVisible'));
  ok(controller.get('isSuccess'));
  equal(controller.get('message'), testMessage);
});
