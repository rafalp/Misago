import assert from 'assert';
import React from 'react'; // jshint ignore:line
import { TabsNav, CompactNav } from 'misago/components/threads/navs'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

let props = {
  lists: [
    {
      path: '',
      name: gettext("All"),
      longName: gettext("All threads")
    },
    {
      path: 'new/',
      name: gettext("New"),
      longName: gettext("New threads")
    }
  ],
  list: {
    path: 'new/',
    name: gettext("New"),
    longName: gettext("New threads")
  }
};

describe("Threads List Navs", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders tab nav", function(done) {
    /* jshint ignore:start */
    testUtils.render(<TabsNav {...props} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .page-tabs', function() {
      assert.ok(true, "component renders");

      props.lists.forEach(function(list, i) {
        let element = $($('#test-mount a')[i]);

        assert.ok(element.length, "list has its link in menu");
        assert.equal(element.find('.hidden-xs').text(), list.name,
          "list has its name in menu");
        assert.equal(element.find('.hidden-md').text(), list.longName,
          "list has its long name in menu");
      });

      done();
    });
  });

  it("renders compact nav", function(done) {
    /* jshint ignore:start */
    testUtils.render(<CompactNav {...props} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .dropdown-menu', function() {
      assert.ok(true, "component renders");

      props.lists.forEach(function(list, i) {
        let element = $($('#test-mount a')[i]);

        assert.ok(element.length, "list has its link in menu");
        assert.equal(element.find('.hidden-xs').text(), list.name,
          "list has its name in menu");
        assert.equal(element.find('.hidden-md').text(), list.longName,
          "list has its long name in menu");
      });

      done();
    });
  });
});
