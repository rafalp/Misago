import assert from 'assert';
import React from 'react'; // jshint ignore:line
import { TabsNav, CompactNav } from 'misago/components/users/navs'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

let lists = {
  baseUrl: '/users/',

  lists: [
    {
      component: "active-posters",
      name: "Active posters"
    },
    {
      component: "rank",
      slug: "admins",
      name: "Admins"
    },
    {
      component: "rank",
      slug: "moderators",
      name: "Moderators"
    }
  ]
};

describe("Users Lists Navs", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders tab nav", function(done) {
    /* jshint ignore:start */
    testUtils.render(<TabsNav {...lists} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .nav-pills', function() {
      assert.ok(true, "component renders");

      lists.lists.forEach(function(list, i) {
        let element = $($('#test-mount a')[i]);

        assert.ok(element.length, "list has its link in menu");
        assert.equal(element.text().trim(), list.name,
          "list has its name in menu");
      });

      done();
    });
  });

  it("renders compact nav", function(done) {
    /* jshint ignore:start */
    testUtils.render(<CompactNav {...lists} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .dropdown-menu', function() {
      assert.ok(true, "component renders");

      lists.lists.forEach(function(list, i) {
        let element = $($('#test-mount a')[i]);

        assert.ok(element.length, "list has its link in menu");
        assert.equal(element.text().trim(), list.name,
          "list has its name in menu");
      });

      done();
    });
  });
});
