import assert from 'assert';
import React from 'react'; // jshint ignore:line
import { SideNav, CompactNav } from 'misago/components/profile/navs'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

let pages = [
  {
    name: 'Followers',
    icon: 'heart',
    component: 'followers',
    meta: {attr: 'test_meta'}
  },
  {
    name: 'Ban details',
    icon: 'lock',
    component: 'ban-details'
  }
];

let profileMock = {
  test_meta: 42,
  is_followed: false,
  acl: {
    can_follow: false,
    can_moderate: false
  }
};

describe("User Profile Side Nav", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    testUtils.render(
      <SideNav baseUrl="/profile/"
               pages={pages}
               profile={profileMock} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .nav-side');

    assert.ok(element.length, "component renders");

    pages.forEach(function(page, i) {
      let link = $(element.find('a')[i]);

      assert.equal(link.find('.material-icon').text(), page.icon,
        "page link contains icon");
      assert.ok(link.text().indexOf(page.name) > 0,
        "page link contains name");

      if (page.meta) {
        assert.equal(link.find('.badge').text(), profileMock.test_meta,
          "page link contains badge");
      }
    });
  });
});

describe("User Profile Compact Nav", function() {
  beforeEach(function() {
    profileMock.acl = {
      can_follow: false,
      can_moderate: false
    };
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    testUtils.render(
      <CompactNav baseUrl="/profile/"
                  pages={pages}
                  profile={profileMock} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .dropdown-menu');

    assert.ok(element.length, "component renders");

    assert.ok(!element.find('.dropdown-buttons').length,
      "component has no special options");

    pages.forEach(function(page, i) {
      let link = $(element.find('a')[i]);

      assert.equal(link.find('.material-icon').text(), page.icon,
        "page link contains icon");
      assert.ok(link.text().indexOf(page.name) > 0,
        "page link contains name");

      if (page.meta) {
        assert.equal(link.find('.badge').text(), profileMock.test_meta,
          "page link contains badge");
      }
    });
  });

  it("renders follow button", function() {
    /* jshint ignore:start */
    profileMock.acl.can_follow = true;
    testUtils.render(
      <CompactNav baseUrl="/profile/"
                  pages={pages}
                  profile={profileMock} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .dropdown-menu .btn-follow');
    assert.ok(element.length, "follow button renders");
  });

  it("renders moderation button", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    let toggleModeration = function() {
      assert.ok(true, "moderation toggle was clicked");

      done();
    }

    profileMock.acl.can_moderate = true;
    testUtils.render(
      <CompactNav baseUrl="/profile/"
                  pages={pages}
                  profile={profileMock}
                  toggleModeration={toggleModeration} />
    );
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .dropdown-menu .btn-block');
  });
});