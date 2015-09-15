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

  QUnit.test("service sets setTitle method on container", function(assert) {
    var service = getMisagoService('page-title');

    var container = {};
    service(container);

    assert.ok(container.setTitle, 'setTitle is set on container');
  });

  QUnit.test("setTitle() call with no arguments sets title to forum name", function(assert) {
    var service = getMisagoService('page-title');

    var container = {settings: {forum_name: 'Lorem Ipsum'}};
    service(container);

    container.setTitle();
    assert.equal(document.title, 'Lorem Ipsum', 'no argument call for setTitle changed title to Lorem Ipsum');
  });

  QUnit.test("setTitle() call with string argument sets valid title", function(assert) {
    var service = getMisagoService('page-title');

    var container = {settings: {forum_name: 'Lorem Ipsum'}};
    service(container);

    container.setTitle("Hello!");
    assert.equal(document.title, 'Hello! | Lorem Ipsum', 'string argument changed title');
  });

  QUnit.test("setTitle() call with object argument sets valid title", function(assert) {
    var service = getMisagoService('page-title');

    var container = {settings: {forum_name: 'Lorem Ipsum'}};
    service(container);

    container.setTitle({title: "Hello!"});
    assert.equal(document.title, 'Hello! | Lorem Ipsum', 'object argument changed title');

    container.setTitle({title: "User", page: 1});
    assert.equal(document.title, 'User | Lorem Ipsum', 'object argument with first page changed title');

    container.setTitle({title: "User", page: 5});
    assert.equal(document.title, 'User (page 5) | Lorem Ipsum', 'object argument with page changed title');

    container.setTitle({title: "User", parent: 'Admins'});
    assert.equal(document.title, 'User | Admins | Lorem Ipsum', 'object argument with parent changed title');

    container.setTitle({title: "User", parent: 'Admins', page: 1});
    assert.equal(document.title, 'User | Admins | Lorem Ipsum', 'object argument with parent and first page changed title');

    container.setTitle({title: "User", parent: 'Admins', page: 5});
    assert.equal(document.title, 'User (page 5) | Admins | Lorem Ipsum', 'object argument with parent and page changed title');

  });
}());
