import Ember from 'ember';
import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('component:routed-links', 'RoutedLinks component');

test('it exists', function(assert) {
  assert.expect(1);

  var component = this.subject();
  assert.ok(component);
});

test('cleanHref validates and cleans hrefs', function(assert) {
  assert.expect(15);

  var router = Ember.Object.create({
    'rootURL': '/misago/'
  });

  var component = this.subject();
  component.set('staticUrl', '/static/');
  component.set('mediaUrl', '/media/');

  var location = window.location;

  // non-forbidden relative url passes
  assert.equal(component.cleanHref(router, '/misago/some-url/'), '/misago/some-url/');

  // protocol relative url passes
  assert.equal(component.cleanHref(router, '//' + location.host + '/misago/some-url/'), '/misago/some-url/');

  // whole url passes
  assert.equal(component.cleanHref(router, 'http://' + location.host + '/misago/some-url/'), '/misago/some-url/');

  // invalid app path fails
  assert.ok(!component.cleanHref(router, '/django/some-url/'));

  // invalid protocol fails
  assert.ok(!component.cleanHref(router, 'https://' + location.host + '/misago/some-url/'));

  // invalid host fails
  assert.ok(!component.cleanHref(router, '//notlocalhost.com/misago/some-url/'));

  // static/media/avatar-server urls fail
  router.set('rootURL', '/');

  assert.ok(!component.cleanHref(router, '/static/some-url/'));
  assert.ok(!component.cleanHref(router, '/media/some-url/'));
  assert.ok(!component.cleanHref(router, '/user-avatar/some-url/'));

  assert.ok(!component.cleanHref(router, '//' + location.host + '/static/some-url/'));
  assert.ok(!component.cleanHref(router, '//' + location.host + '/media/some-url/'));
  assert.ok(!component.cleanHref(router, '//' + location.host + '/user-avatar/some-url/'));

  assert.ok(!component.cleanHref(router, 'http://' + location.host + '/static/some-url/'));
  assert.ok(!component.cleanHref(router, 'http://' + location.host + '/media/some-url/'));
  assert.ok(!component.cleanHref(router, 'http://' + location.host + '/user-avatar/some-url/'));
});
