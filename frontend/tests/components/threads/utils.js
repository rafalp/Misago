import assert from 'assert';
import { getPageTitle, getTitle, getModerationActions } from 'misago/components/threads/utils';
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

describe("Threads List Moderation Actions Util", function() {
  it("shows no moderation for no threads", function() {
    const moderationActions = getModerationActions([]);

    assert.ok(!moderationActions.allow, "moderation is unavaiable");
  });

  it("shows no moderation for unmoderable threads", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: false,
          can_close: false,
          can_hide: false,
          can_merge: false,
          can_move: false,
          can_pin: false
        },
        is_unapproved: false
      }
    ]);

    assert.ok(!moderationActions.allow, "moderation is unavaiable");
  });

  it("shows moderation for unapproved approvable thread", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: true,
          can_close: false,
          can_hide: false,
          can_merge: false,
          can_move: false,
          can_pin: false
        },
        is_unapproved: true
      }
    ]);

    assert.ok(moderationActions.allow, "moderation is allowed");
    assert.ok(moderationActions.can_approve, "approve action is available");
  });

  it("shows no moderation for approved approvable thread", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: true,
          can_close: false,
          can_hide: false,
          can_merge: false,
          can_move: false,
          can_pin: false
        },
        is_unapproved: false
      }
    ]);

    assert.ok(!moderationActions.allow, "moderation is unavaiable");
    assert.ok(!moderationActions.can_approve, "approve action is unavaiable");
  });

  it("shows moderation for closing thread", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: false,
          can_close: true,
          can_hide: false,
          can_merge: false,
          can_move: false,
          can_pin: false
        },
        is_unapproved: false
      }
    ]);

    assert.ok(moderationActions.allow, "moderation is allowed");
    assert.ok(moderationActions.can_close, "close action is available");
  });

  it("shows moderation for hiding thread", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: false,
          can_close: false,
          can_hide: 1,
          can_merge: false,
          can_move: false,
          can_pin: false
        },
        is_unapproved: false
      }
    ]);

    assert.ok(moderationActions.allow, "moderation is allowed");
    assert.equal(moderationActions.can_hide, 1, "delete action is available");
  });

  it("shows moderation for deleting thread", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: false,
          can_close: false,
          can_hide: 2,
          can_merge: false,
          can_move: false,
          can_pin: false
        },
        is_unapproved: false
      }
    ]);

    assert.ok(moderationActions.allow, "moderation is allowed");
    assert.equal(moderationActions.can_hide, 2, "delete action is available");
  });

  it("shows moderation for mergin thread", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: false,
          can_close: false,
          can_hide: false,
          can_merge: true,
          can_move: false,
          can_pin: false
        },
        is_unapproved: false
      }
    ]);

    assert.ok(moderationActions.allow, "moderation is allowed");
    assert.ok(moderationActions.can_merge, "merge action is available");
  });

  it("shows moderation for moving thread", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: false,
          can_close: false,
          can_hide: false,
          can_merge: false,
          can_move: true,
          can_pin: false
        },
        is_unapproved: false
      }
    ]);

    assert.ok(moderationActions.allow, "moderation is allowed");
    assert.ok(moderationActions.can_move, "move action is available");
  });

  it("shows moderation for pinning thread", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: false,
          can_close: false,
          can_hide: false,
          can_merge: false,
          can_move: false,
          can_pin: 1
        },
        is_unapproved: false
      }
    ]);

    assert.ok(moderationActions.allow, "moderation is allowed");
    assert.equal(moderationActions.can_pin, 1, "pin action is available");
  });

  it("shows moderation for pinning thread globally", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: false,
          can_close: false,
          can_hide: false,
          can_merge: false,
          can_move: false,
          can_pin: 2
        },
        is_unapproved: false
      }
    ]);

    assert.ok(moderationActions.allow, "moderation is allowed");
    assert.equal(moderationActions.can_pin, 2, "pin action is available");
  });

  it("shows moderation kitchensink", function() {
    const moderationActions = getModerationActions([
      {
        acl: {
          can_approve: true,
          can_close: true,
          can_hide: 2,
          can_merge: true,
          can_move: true,
          can_pin: 2
        },
        is_unapproved: true
      }
    ]);

    assert.deepEqual(moderationActions, {
      allow: true,

      can_approve: true,
      can_close: true,
      can_hide: 2,
      can_merge: true,
      can_move: true,
      can_pin: 2
    }, "moderation is allowed");
  });
});