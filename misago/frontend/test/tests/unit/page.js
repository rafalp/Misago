(function (Misago) {
  'use strict';

  QUnit.module("Page");

  QUnit.test("page name", function(assert) {
    var page = new Misago.Page('test page', {});

    assert.equal(page.name, 'test page',
      'new page was created with valid name.');
  });

  QUnit.test("add and read sections", function(assert) {
    var page = new Misago.Page('test page', {});

    page.addSection({
      name: 'Apples',
      link: 'page_apples'
    });
    page.addSection({
      name: 'Oranges',
      link: 'page_oranges',
      before: 'page_apples'
    });

    var sections = page.getSections();

    assert.deepEqual(sections, [
        {
          name: 'Oranges',
          link: 'page_oranges',
          before: 'page_apples'
        },
        {
          name: 'Apples',
          link: 'page_apples'
        }
      ],
      "page service returned sorted sections.");

    assert.equal(page.getDefaultLink(), 'page_oranges',
      "page has valid default link.");
  });
}(Misago.prototype));
