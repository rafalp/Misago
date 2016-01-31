import assert from 'assert';
import React from 'react'; // jshint ignore:line
import { SideNav, CompactNav } from 'misago/components/options/navs'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

let options = {
  baseUrl: '/options/',

  options: [
    {
      component: "forum-options",
      icon: "settings",
      name: "Forum options"
    },
    {
      component: "change-username",
      icon: "card_membership",
      name: "Change username"
    },
    {
      component: "sign-in-credentials",
      icon: "vpn_key",
      name: "Change sign-in credentials"
    }
  ]
};

describe("Options Navs", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders side nav", function(done) {
    /* jshint ignore:start */
    testUtils.render(<SideNav {...options} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .nav-side', function() {
      assert.ok(true, "component renders");

      options.options.forEach(function(option, i) {
        let element = $($('#test-mount a')[i]);

        assert.ok(element.length, "option has its link in menu");
        assert.equal(element.find('.material-icon').text().trim(), option.icon,
          "option has its icon in menu");
        assert.ok(element.text().indexOf(option.name) !== -1,
          "option has its name in menu");
      });

      done();
    });
  });

  it("renders compact nav", function(done) {
    /* jshint ignore:start */
    testUtils.render(<CompactNav {...options} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .dropdown-menu', function() {
      assert.ok(true, "component renders");

      options.options.forEach(function(option, i) {
        let element = $($('#test-mount a')[i]);

        assert.ok(element.length, "option has its link in menu");
        assert.equal(element.find('.material-icon').text().trim(), option.icon,
          "option has its icon in menu");
        assert.ok(element.text().indexOf(option.name) !== -1,
          "option has its name in menu");
      });

      done();
    });
  });
});
