import Ember from 'ember';
import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('controller:login-modal', 'LoginModalController');

test('it exists', function(assert) {
  assert.expect(1);

  var self = this;
  Ember.run(function(){
    var controller = self.subject();
    assert.ok(controller);
  });
});

test('reset works', function(assert) {
  assert.expect(8);

  var self = this;
  Ember.run(function(){
    var controller = self.subject();

    controller.set('username', 'TestUsername');
    controller.set('password', 'secretpassword');

    controller.set('isLoading', true);
    controller.set('showActivation', true);

    assert.equal(controller.get('username'), 'TestUsername');
    assert.equal(controller.get('password'), 'secretpassword');

    assert.equal(controller.get('isLoading'), true);
    assert.equal(controller.get('showActivation'), true);

    controller.reset();

    assert.equal(controller.get('username'), '');
    assert.equal(controller.get('password'), '');

    assert.equal(controller.get('isLoading'), false);
    assert.equal(controller.get('showActivation'), false);
  });
});
