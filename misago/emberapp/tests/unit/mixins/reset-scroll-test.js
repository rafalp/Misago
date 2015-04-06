import Ember from 'ember';
import ResetScrollMixin from '../../../mixins/reset-scroll';
import { module, test } from 'qunit';

module('ResetScrollMixin');

test('it works', function(assert) {
  assert.expect(1);

  var ResetScrollObject = Ember.Object.extend(ResetScrollMixin);
  var subject = ResetScrollObject.create();
  assert.ok(subject);
});
