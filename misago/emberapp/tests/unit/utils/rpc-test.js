import Ember from 'ember';
import { default as rpc, buildUrl, ajax } from '../../../utils/rpc';
import { module, test } from 'qunit';

module('RPC', {
  afterEach: function() {
    Ember.$.mockjax.clear();
  }
});

test('buildUrl builds valid urls', function(assert) {
  assert.expect(3);

  assert.equal(buildUrl('some/procedure', {
    API_HOST: '',
    API_NAMESPACE: 'api/v2',
    API_ADD_TRAILING_SLASHES: true
  }), '/api/v2/some/procedure/');

  assert.equal(buildUrl('some/procedure', {
    API_HOST: '',
    API_NAMESPACE: 'api/v2',
    API_ADD_TRAILING_SLASHES: false
  }), '/api/v2/some/procedure');

  assert.equal(buildUrl('some/procedure', {
    API_HOST: 'https://api.testsite.com',
    API_NAMESPACE: 'api/v2',
    API_ADD_TRAILING_SLASHES: false
  }), 'https://api.testsite.com/api/v2/some/procedure');
});

var conf = {
  API_HOST: '',
  API_NAMESPACE: 'api',
  API_ADD_TRAILING_SLASHES: true
};

test('successfull rpc call passes', function(assert) {
  assert.expect(1);
  var done = assert.async();

  Ember.$.mockjax({
    url: "/api/some-rpc/",
    status: 200,
    responseText: {
      'detail': 'it works'
    }
  });

  rpc('some-rpc', {}, conf).then(function(data) {
    assert.equal(data.detail, 'it works');
  }, function() {
    assert.fail("rpc call should pass");
  }).finally(function() {
    done();
  });
});

test('invalid rpc call fails', function(assert) {
  assert.expect(1);
  var done = assert.async();

  Ember.$.mockjax({
    url: "/api/some-rpc/",
    status: 400,
    responseText: {
      'detail': 'nope'
    }
  });

  rpc('some-rpc', {}, conf).then(function() {
    assert.fail("rpc call should fail");
  }, function(jqXHR) {
    assert.equal(jqXHR.responseJSON.detail, 'nope');
  }).finally(function() {
    done();
  });
});
