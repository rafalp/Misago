import Ember from 'ember';
import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('component:login-modal', 'LoginModalComponent');

test('it exists', function(assert) {
  assert.expect(1);

  var self = this;
  Ember.run(function(){
    var component = self.subject();
    assert.ok(component);
  });
});

test('reset works', function(assert) {
  assert.expect(8);

  var self = this;
  Ember.run(function(){
    var component = self.subject();

    component.set('username', 'TestUsername');
    component.set('password', 'secretpassword');

    component.set('isLoading', true);
    component.set('showActivation', true);

    assert.equal(component.get('username'), 'TestUsername');
    assert.equal(component.get('password'), 'secretpassword');

    assert.equal(component.get('isLoading'), true);
    assert.equal(component.get('showActivation'), true);

    component.reset();

    assert.equal(component.get('username'), '');
    assert.equal(component.get('password'), '');

    assert.equal(component.get('isLoading'), false);
    assert.equal(component.get('showActivation'), false);
  });
});
