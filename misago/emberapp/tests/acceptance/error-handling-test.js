import Ember from 'ember';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: Application Error Handler', {
  setup: function() {
    application = startApp();
  },
  teardown: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('some unhandled error occured', function() {
  Ember.$.mockjax({
    url: "/api/legal-pages/privacy-policy/",
    status: 500,
    responseText: {
      'detail': 'The kek'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    equal(currentPath(), 'error');
  });
});

test('app went away', function() {
  Ember.$.mockjax({
    url: "/api/legal-pages/privacy-policy/",
    status: 0,
    responseText: {
      'detail': 'Connection rejected'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    equal(currentPath(), 'error-0');
  });
});

test('not found', function() {
  Ember.$.mockjax({
    url: "/api/legal-pages/privacy-policy/",
    status: 404,
    responseText: {
      'detail': 'Not found'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    equal(currentPath(), 'error-404');
  });
});

test('permission denied', function() {
  Ember.$.mockjax({
    url: "/api/legal-pages/privacy-policy/",
    status: 403,
    responseText: {
      'detail': 'Permission denied'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    equal(currentPath(), 'error-403');
  });
});

test('permission denied with reason', function() {
  Ember.$.mockjax({
    url: "/api/legal-pages/privacy-policy/",
    status: 403,
    responseText: {
      'detail': 'Lorem ipsum dolor met.'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    equal(currentPath(), 'error-403');
    var $e = find('.lead');
    equal(Ember.$.trim($e.text()), 'Lorem ipsum dolor met.');
  });
});

test('not found route', function() {
  visit('/this-url-really-doesnt-exist');

  andThen(function() {
    equal(currentPath(), 'error-404');
  });
});
