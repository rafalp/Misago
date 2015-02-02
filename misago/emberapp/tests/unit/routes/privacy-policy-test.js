import {
  moduleFor,
  test
} from 'ember-qunit';

var document_title = document.title;

moduleFor('route:privacy-policy', 'PrivacyPolicyRoute', {
  teardown: function() {
    document.title = document_title;
  }
});

test('it exists', function() {
  var route = this.subject();
  ok(route);
});

test('setting', function() {
  var route = this.subject();
  equal(route.get('setting'), 'privacy_policy');
});

test('title', function() {
  var route = this.subject();

  equal(route.get('title'), route.get('defaultTitle'));

  var testTitle = "Lorem Ipsum Dolor Met";
  route.set("settings", {'privacy_policy_title': testTitle});
  equal(route.get('title'), testTitle);
});

test('link', function() {
  var route = this.subject();

  ok(!route.get('link'));

  var testLink = "http://somewhere.com";
  route.set("settings", {'privacy_policy_link': testLink});
  equal(route.get('link'), testLink);
});
