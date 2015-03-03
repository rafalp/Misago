import Ember from 'ember';
import { initialize } from '../../../initializers/moment-locale';
import { module, test } from 'qunit';

var container, application;
var documentLang = null;

module('MomentLocaleInitializer', {
  beforeEach: function() {
    documentLang = Ember.$('html').attr('lang');

    Ember.run(function() {
      application = Ember.Application.create();
      container = application.__container__;
      application.deferReadiness();
    });
  },

  afterEach: function() {
    Ember.$('html').attr('lang', documentLang);
    moment.locale(documentLang);
  }
});

test('initializer changes moment.js locale', function(assert) {
  Ember.$('html').attr('lang', 'pl');
  initialize(container, application);

  assert.equal(moment.locale(), 'pl');
});
