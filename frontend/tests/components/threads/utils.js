import assert from 'assert';
import { getPageTitle, getTitle } from 'misago/components/threads/utils';
import misago from 'misago/index';

describe("Threads List Title Utils", function() {
  beforeEach(function() {
    // set default title
    misago._context = {
      CATEGORIES_ON_INDEX: false,

      SETTINGS: {
        forum_index_title: "",
        forum_name: "Test forum"
      }
    };
  });

  it("getPageTitle returns valid obj for title service", function() {
    assert.deepEqual(getPageTitle({
      list: {
        longName: "",
        path: ''
      },
      category: {
        name: "Test category"
      }
    }), {
      title: "Test category"
    }, "nonspecial category's name is returned");

    assert.deepEqual(getPageTitle({
      list: {
        longName: "New threads",
        path: 'new/'
      },
      category: {
        name: "Test category"
      }
    }), {
      title: "New threads",
      parent: "Test category"
    }, "list name under category name is returned");

    assert.equal(getPageTitle({
      list: {
        longName: "Threads",
        path: ''
      },
      category: {
        name: "Root",
        special_role: true
      }
    }), null, "null is returned for special category");

    assert.deepEqual(getPageTitle({
      list: {
        longName: "New threads",
        path: 'new/'
      },
      category: {
        name: "Root",
        special_role: true
      }
    }), {
      title: "New threads"
    }, "list name is returned for special category");

    misago._context.CATEGORIES_ON_INDEX = true;
    assert.deepEqual(getPageTitle({
      list: {
        longName: "",
        path: ''
      },
      category: {
        name: "Root",
        special_role: true
      }
    }), {
      title: "Threads"
    }, "fallback title is returned for special category");

    assert.deepEqual(getPageTitle({
      list: {
        longName: "New threads",
        path: 'new/'
      },
      category: {
        name: "Root",
        special_role: true
      }
    }), {
      title: "New threads",
      parent: "Threads"
    }, "list title under fallback is returned for special category");
  });

  it("getTitle returns valid title for header", function() {
    assert.equal(getTitle({
      category: {
        name: "Test category"
      }
    }), "Test category", "nonspecial category's name is returned as title");

    assert.equal(getTitle({
      category: {
        name: "Root",
        special_role: true
      }
    }), "Test forum", "forum name was used for title instead of category's");

    misago._context.SETTINGS.forum_index_title = "Forum index";
    assert.equal(getTitle({
      category: {
        name: "Root",
        special_role: true
      }
    }), "Forum index", "index title was used for title instead of category's");

    misago._context.CATEGORIES_ON_INDEX = true;
    assert.equal(getTitle({
      category: {
        name: "Root",
        special_role: true
      }
    }), "Threads", "fallback title was used for forum threads list");
  });
});
