import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Header from 'misago/components/threads/header'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

let route = null;

describe("Threads List Header", function() {
  beforeEach(function() {
    route = {
      lists: [],
      list: {
        name: "All",
        nameLong: "All threads",
        path: ''
      },
      category: {
        name: "Root",
        parent: null
      }
    };
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders title", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Header route={route} title="Lorem Ipsum" user={{id: null}} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .page-header h1');
    assert.ok(element.length, "component renders");
    assert.equal(element.text(), "Lorem Ipsum", "heading has valid text");
  });

  it("renders without nav", function() {
    /* jshint ignore:start */
    testUtils.render(<Header route={route} title="Test" user={{id: null}} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header');
    assert.ok(element.length, "component renders");
    assert.ok(!element.hasClass('tabbed'), "tabbed class is not present");

    assert.ok(!element.find('.page-tabs').length, "tabs are hidden");
    assert.ok(!element.find('.btn').length, "toggle nav button is hidden");
  });

  it("renders with nav", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    route = {
      lists: [
        {
          name: "All",
          nameLong: "All threads",
          path: ''
        },
        {
          name: "New",
          nameLong: "New threads",
          path: 'new/'
        }
      ],
      list: {
        name: "All",
        nameLong: "All threads",
        path: ''
      },
      category: {
        name: "Root",
        parent: null
      }
    };

    let callback = function() {
      assert.ok(true, "toggleNav() was called");
      done();
    };

    testUtils.render(
      <Header route={route}
              title="Test"
              toggleNav={callback}
              user={{id: null}} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .page-header');
    assert.ok(element.length, "heading renders");
    assert.ok(element.hasClass('tabbed'), "tabbed class is not present");

    assert.ok(element.find('.page-tabs').length, "tabs are hidden");
    assert.ok(element.find('.btn').length, "toggle nav button is hidden");

    testUtils.simulateClick('#test-mount .btn-dropdown-toggle');
  });

  it("renders go back button", function() {
    /* jshint ignore:start */
    route.list= {
      name: "New",
      nameLong: "New threads",
      path: 'new/'
    };
    route.category.parent = {
      name: "Parent",
      absolute_url: '/parent-12/'
    }
    testUtils.render(<Header route={route} title="Test"  user={{id: null}} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header .btn-go-back');
    assert.ok(element.length, "button renders");
  });

  it("renders new thread button for authenticated", function() {
    /* jshint ignore:start */
    route.list= {
      name: "New",
      nameLong: "New threads",
      path: 'new/'
    };
    route.category.parent = {
      name: "Parent",
      absolute_url: '/parent-12/'
    }
    testUtils.render(<Header route={route} title="Test"  user={{id: null}} />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-header .btn-success');
    assert.ok(!element.length, "button is hidden for guest");

    /* jshint ignore:start */
    testUtils.render(<Header route={route} title="Test"  user={{id: 123}} />);
    /* jshint ignore:end */

    element = $('#test-mount .page-header .btn-success');
    assert.ok(element.length, "button is rendered for authenticated");
  });
});
