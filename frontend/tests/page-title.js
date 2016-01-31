import assert from 'assert';
import title from 'misago/services/page-title';

describe('Page Title', function() {
  beforeEach(function() {
    title.init('Test Forum');
  });

  it("sets title", function() {
    title.set("Lorem ipsum");
    assert.equal(document.title, "Lorem ipsum | Test Forum",
      "string argument is used to set title");

    title.set({
      title: "Lorem ipsum"
    });
    assert.equal(document.title, "Lorem ipsum | Test Forum",
      "object with title prop is used to set title");

    title.set({
      title: "Lorem ipsum",
      parent: "Dolor met"
    });
    assert.equal(document.title, "Lorem ipsum | Dolor met | Test Forum",
      "object with title and parent props is used to set valid title");

    title.set({
      title: "Lorem ipsum",
      page: 4
    });
    assert.equal(document.title, "Lorem ipsum (page 4) | Test Forum",
      "object with title and page props is used to set valid title");

    title.set({
      title: "Lorem ipsum",
      parent: "Dolor",
      page: 4
    });
    assert.equal(document.title, "Lorem ipsum (page 4) | Dolor | Test Forum",
      "object with title, parent and page props is used to set valid title");
  });
});