import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import AuthMessage from 'misago/components/auth-message'; // jshint ignore:line

describe("Auth Message", function() {
  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders stateless', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <AuthMessage />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount .auth-message');
    assert.ok(element.length, "component renders when its stateless");
    assert.ok(!element.hasClass('show'), "component is hidden");
  });

  it('renders signed out', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <AuthMessage user={{username: 'Boberson'}}
                   signedOut={true}
                   signedIn={false} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount .auth-message');
    assert.ok(element.length, "component renders for signed out");
    assert.ok(element.hasClass('show'), "component is visible");
  });

  it('renders signed in', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <AuthMessage user={null}
                   signedOut={false}
                   signedIn={{username: 'Boberson'}} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount .auth-message');
    assert.ok(element.length, "component renders for signed in");
    assert.ok(element.hasClass('show'), "component is visible");
  });
});
