(function () {
  'use strict';

  var orgTitle = document.title;

  QUnit.module("Page Title", {
    beforeEach: function() {
      orgTitle = document.title;
    },
    afterEach: function() {
      document.title = orgTitle;
    }
  });

  QUnit.test("service sets title.set method on container", function(assert) {
    var service = getMisagoService('page-title');

    var container = {settings: {forum_name: 'Lorem Ipsum'}};
    service(container);

    assert.ok(container.title.set, 'title.set is set on container');
  });

  QUnit.test("title.set() call with no arguments sets title to forum name", function(assert) {
    var service = getMisagoService('page-title');

    var container = {settings: {forum_name: 'Lorem Ipsum'}};
    service(container);

    container.title.set();
    assert.equal(document.title, 'Lorem Ipsum', 'no argument call for title.set changed title to Lorem Ipsum');
  });

  QUnit.test("title.set() call with string argument sets valid title", function(assert) {
    var service = getMisagoService('page-title');

    var container = {settings: {forum_name: 'Lorem Ipsum'}};
    service(container);

    container.title.set("Hello!");
    assert.equal(document.title, 'Hello! | Lorem Ipsum', 'string argument changed title');
  });

  QUnit.test("title.set() call with object argument sets valid title", function(assert) {
    var service = getMisagoService('page-title');

    var container = {settings: {forum_name: 'Lorem Ipsum'}};
    service(container);

    container.title.set({title: "Hello!"});
    assert.equal(document.title, 'Hello! | Lorem Ipsum', 'object argument changed title');

    container.title.set({title: "User", page: 1});
    assert.equal(document.title, 'User | Lorem Ipsum', 'object argument with first page changed title');

    container.title.set({title: "User", page: 5});
    assert.equal(document.title, 'User (page 5) | Lorem Ipsum', 'object argument with page changed title');

    container.title.set({title: "User", parent: 'Admins'});
    assert.equal(document.title, 'User | Admins | Lorem Ipsum', 'object argument with parent changed title');

    container.title.set({title: "User", parent: 'Admins', page: 1});
    assert.equal(document.title, 'User | Admins | Lorem Ipsum', 'object argument with parent and first page changed title');

    container.title.set({title: "User", parent: 'Admins', page: 5});
    assert.equal(document.title, 'User (page 5) | Admins | Lorem Ipsum', 'object argument with parent and page changed title');

  });
}());
