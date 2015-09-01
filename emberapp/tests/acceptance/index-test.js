import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: Index', {
  beforeEach: function() {
    application = startApp();
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
  }
});

test('visiting /', function(assert) {
  assert.expect(1);

  visit('/');

  andThen(function() {
    assert.equal(currentPath(), 'index');
  });
});

test('visiting / with custom title', function(assert) {
  assert.expect(2);

  var newTitle = "Misago Support Forums";
  window.MisagoData.misagoSettings['forum_index_title'] = newTitle;
  visit('/');

  andThen(function() {
    assert.equal(currentPath(), 'index');
    assert.equal(document.title, newTitle);
  });
});
