import {
  moduleFor,
  test
} from 'ember-qunit';

var document_title = document.title;

moduleFor('route:terms-of-service', 'TermsOfServiceRoute', {
  afterEach: function() {
    document.title = document_title;
  }
});

test('it exists', function(assert) {
  assert.expect(1);

  var route = this.subject();
  assert.ok(route);
});

test('setting', function(assert) {
  assert.expect(1);

  var route = this.subject();
  assert.equal(route.get('setting'), 'terms_of_service');
});

test('title', function(assert) {
  assert.expect(2);

  var route = this.subject();

  assert.equal(route.get('title'), route.get('defaultTitle'));

  var testTitle = "Lorem Ipsum Dolor Met";
  route.set("settings", {'terms_of_service_title': testTitle});
  assert.equal(route.get('title'), testTitle);
});

test('link', function(assert) {
  assert.expect(2);

  var route = this.subject();

  assert.ok(!route.get('link'));

  var testLink = "http://somewhere.com";
  route.set("settings", {'terms_of_service_link': testLink});
  assert.equal(route.get('link'), testLink);
});
