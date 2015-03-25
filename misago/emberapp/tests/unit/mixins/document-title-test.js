import Ember from 'ember';
import DocumentTitleMixin from '../../../mixins/document-title';
import { module, test } from 'qunit';

var title;

module('DocumentTitleMixin', {
  beaforeEach: function() {
    title = document.title;
  },

  afterEach: function() {
    document.title = title;
  }
});

// Replace this with your real tests.
test('it works', function(assert) {
  var DocumentTitleObject = Ember.Object.extend(DocumentTitleMixin);
  var subject = DocumentTitleObject.create();
  assert.ok(subject);
});
