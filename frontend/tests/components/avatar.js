import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Avatar", function() {
  afterEach(function() {
    testUtils.emptyTestContainers();
  });

  it('renders guest avatar', function() {
    /* jshint ignore:start */
    testUtils.render(<Avatar size="42" />, 'test-mount');
    /* jshint ignore:end */

    let element = $('#test-mount img.user-avatar');
    assert.ok(element.length, "component renders for guest");
    assert.equal(element.attr('src'), '/test-runner/user-avatar/42.png', "component builds valid avatar url");
  });

  it('renders user avatar', function() {
    /* jshint ignore:start */
    let user = {
      id: 1234,
      avatar_hash: 'aabbccddeeff'
    };

    testUtils.render(<Avatar user={user} size="42" />, 'test-mount');
    /* jshint ignore:end */

    let element = $('#test-mount img.user-avatar');
    assert.ok(element.length, "component renders for user");
    assert.equal(element.attr('src'), '/test-runner/user-avatar/aabbccddeeff/42/1234.png',
      "component builds valid avatar url for authenticated");
  });
});
