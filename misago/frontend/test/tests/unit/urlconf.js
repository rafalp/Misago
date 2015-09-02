(function (Misago) {
  'use strict';

  var urlconf = null;

  QUnit.module("UrlConf", {
    beforeEach: function() {
      urlconf = new Misago.UrlConf();
    }
  });

  QUnit.test("UrlConf.url registers pattern in config", function(assert) {
    var component = {test: 'test'};

    urlconf.url('/test/', component, 'test_url');
    var patterns = urlconf.patterns();

    assert.equal(patterns.length, 1, 'url() has registered single URL in config');
    assert.deepEqual(patterns[0],
                     {pattern: '/test/', component: component, name: 'test_url'},
                     'url() has registered valid URL in config');
  });

  QUnit.test("UrlConf.url(conf) includes child config", function(assert) {
    var component = {test: 'test'};
    urlconf.url('', component, 'test_url');
    urlconf.url('/test/', component, 'test_url');

    var childconf = new Misago.UrlConf();
    childconf.url('/', component, 'users');
    childconf.url('/user/', component, 'user');

    urlconf.url('/users/', childconf);

    var expected_patterns = [
      {pattern: '/', component: component, name: 'test_url'},
      {pattern: '/test/', component: component, name: 'test_url'},
      {pattern: '/users/', component: component, name: 'users'},
      {pattern: '/users/user/', component: component, name: 'user'}
    ];

    assert.deepEqual(urlconf.patterns(), expected_patterns,
                     'url() has included other urlconf');
  });
}(Misago.prototype));
