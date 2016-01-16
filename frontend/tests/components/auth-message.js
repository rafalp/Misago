import assert from 'assert';
import React from 'react'; // jshint ignore:line
import AuthMessage from 'misago/components/auth-message'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Auth Message", function() {
  afterEach(function() {
    testUtils.emptyTestContainers();
  });

  it('renders stateless', function() {
    /* jshint ignore:start */
    testUtils.render(<AuthMessage />, 'test-mount');
    /* jshint ignore:end */

    let element = $('#test-mount .auth-message');
    assert.ok(element.length, "component renders when its stateless");
    assert.ok(!element.hasClass('show'), "component is hidden");
  });

  it('renders signed out', function() {
    /* jshint ignore:start */
    testUtils.render(
      <AuthMessage user={{username: 'Boberson'}}
                   signedOut={true}
                   signedIn={false} />,
      'test-mount'
    );
    /* jshint ignore:end */

    let element = $('#test-mount .auth-message');
    assert.ok(element.length, "component renders for signed out");
    assert.ok(element.hasClass('show'), "component is visible");
  });

  it('renders signed in', function() {
    /* jshint ignore:start */
    testUtils.render(
      <AuthMessage user={null}
                   signedOut={false}
                   signedIn={{username: 'Boberson'}} />,
      'test-mount'
    );
    /* jshint ignore:end */

    let element = $('#test-mount .auth-message');
    assert.ok(element.length, "component renders for signed in");
    assert.ok(element.hasClass('show'), "component is visible");
  });
});
