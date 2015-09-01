import Ember from 'ember';
import DS from 'ember-data';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application, container, service;

module('Acceptance: Ajax Service', {
  beforeEach: function() {
    application = startApp();
    container = application.__container__;
    service = container.lookup('service:ajax');
  },

  afterEach: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('unpluralizeUrlProcedure fixes urls', function(assert) {
  assert.expect(3);

  var url = service.unpluralizeUrlProcedure('/some-words/', 'some-word');
  assert.equal(url, '/some-word/');

  url = service.unpluralizeUrlProcedure('/some-words/', 'someWord');
  assert.equal(url, '/some-word/');

  url = service.unpluralizeUrlProcedure('/model/some-words/', 'some-word');
  assert.equal(url, '/model/some-word/');
});

test('buildProcedureURL builds valid url', function(assert) {
  assert.expect(4);

  var adapter = container.lookup('adapter:application');

  var url = service.buildProcedureURL(adapter, 'close');
  assert.equal(url, '/api/close/');

  url = service.buildProcedureURL(adapter, 'close-thread');
  assert.equal(url, '/api/close-thread/');

  url = service.buildProcedureURL(adapter, 'closeThread');
  assert.equal(url, '/api/close-thread/');

  url = service.buildProcedureURL(adapter, 'thread/1/close');
  assert.equal(url, '/api/thread/1/close/');
});

test('successful get', function(assert) {
  assert.expect(2);
  var done = assert.async();

  Ember.$.mockjax({
    url: '/api/some-value/',
    status: 200,
    responseText: {
      'detail': 'it works'
    }
  });

  service.get('some-value').then(function(data) {
    assert.equal(data.detail, 'it works');
  }, function() {
    assert.ok(false, 'get call should pass');
  }).finally(function() {
    assert.ok(true, 'finally() was called');
    done();
  });
});

test('failed post', function(assert) {
  assert.expect(2);
  var done = assert.async();

  Ember.$.mockjax({
    url: '/api/some-value/',
    status: 400,
    responseText: {
      'detail': 'it fails'
    }
  });

  service.get('some-value').then(function(data) {
    assert.ok(false, 'get call should fail');
  }, function(jqXHR) {
    var rejection = jqXHR.responseJSON;
    assert.equal(rejection.detail, 'it fails');
  }).finally(function() {
    assert.ok(true, 'finally() was called');
    done();
  });
});

test('successful model prop get', function(assert) {
  assert.expect(2);
  var done = assert.async();

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 200,
    responseText: {
      'id': 'privacy-policy',
      'title': '',
      'link': '',
      'body': ''
    }
  });

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/some-rpc/',
    status: 200,
    responseText: {
      'detail': 'it works'
    }
  });

  Ember.run(function() {
    var store = container.lookup('store:main');

    store.find('legal-page', 'privacy-policy').then(function(record) {
      service.get(record, 'some-rpc').then(function(data) {
        assert.equal(data.detail, 'it works');
      }, function() {
        assert.ok(false, 'model get call should pass');
      }).finally(function() {
        assert.ok(true, 'finally() was called');
        done();
      });
    });
  });
});

test('failed model prop get', function(assert) {
  assert.expect(2);
  var done = assert.async();

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 200,
    responseText: {
      'id': 'privacy-policy',
      'title': '',
      'link': '',
      'body': ''
    }
  });

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/some-rpc/',
    status: 400,
    responseText: {
      'detail': 'it failed'
    }
  });

  Ember.run(function() {
    var store = container.lookup('store:main');

    store.find('legal-page', 'privacy-policy').then(function(record) {
      service.get(record, 'some-rpc').then(function() {
        assert.ok(false, 'get call should fail');
      }, function(jqXHR) {
        var rejection = jqXHR.responseJSON;
        assert.equal(rejection.detail, 'it failed');
      }).finally(function() {
        assert.ok(true, 'finally() was called');
        done();
      });
    });
  });
});

test('successful post', function(assert) {
  assert.expect(2);
  var done = assert.async();

  Ember.$.mockjax({
    url: '/api/some-rpc/',
    status: 200,
    responseText: {
      'detail': 'it works'
    }
  });

  service.post('some-rpc').then(function(data) {
    assert.equal(data.detail, 'it works');
  }, function() {
    assert.ok(false, 'rpc call should pass');
  }).finally(function() {
    assert.ok(true, 'finally() was called');
    done();
  });
});

test('failed post', function(assert) {
  assert.expect(2);
  var done = assert.async();

  Ember.$.mockjax({
    url: '/api/some-rpc/',
    status: 400,
    responseText: {
      'detail': 'it fails'
    }
  });

  service.post('some-rpc').then(function() {
    assert.ok(false, 'rpc call should fail');
  }, function(jqXHR) {
    var rejection = jqXHR.responseJSON;
    assert.equal(rejection.detail, 'it fails');
  }).finally(function() {
    assert.ok(true, 'finally() was called');
    done();
  });
});

test('successful model rpc post', function(assert) {
  assert.expect(2);
  var done = assert.async();

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 200,
    responseText: {
      'id': 'privacy-policy',
      'title': '',
      'link': '',
      'body': ''
    }
  });

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/some-rpc/',
    status: 200,
    responseText: {
      'detail': 'it works'
    }
  });

  Ember.run(function() {
    var store = container.lookup('store:main');

    store.find('legal-page', 'privacy-policy').then(function(record) {
      service.post(record, 'some-rpc').then(function(data) {
        assert.equal(data.detail, 'it works');
      }, function() {
        assert.ok(false, 'rpc call should pass');
      }).finally(function() {
        assert.ok(true, 'finally() was called');
        done();
      });
    });
  });
});

test('failed model rpc post', function(assert) {
  assert.expect(2);
  var done = assert.async();

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 200,
    responseText: {
      'id': 'privacy-policy',
      'title': '',
      'link': '',
      'body': ''
    }
  });

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/some-rpc/',
    status: 400,
    responseText: {
      'detail': 'it failed'
    }
  });

  Ember.run(function() {
    var store = container.lookup('store:main');

    store.find('legal-page', 'privacy-policy').then(function(record) {
      service.post(record, 'some-rpc').then(function() {
        assert.ok(false, 'rpc call should fail');
      }, function(jqXHR) {
        var rejection = jqXHR.responseJSON;
        assert.equal(rejection.detail, 'it failed');
      }).finally(function() {
        assert.ok(true, 'finally() was called');
        done();
      });
    });
  });
});
