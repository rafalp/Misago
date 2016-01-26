import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Li from 'misago/components/li'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Li", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders', function() {
    /* jshint ignore:start */
    testUtils.render(<Li />);
    /* jshint ignore:end */

    let element = $('#test-mount li');
    assert.ok(element.length, "component renders");
  });

  it('renders with class name', function() {
    /* jshint ignore:start */
    testUtils.render(<Li className="test-class" />);
    /* jshint ignore:end */

    let element = $('#test-mount li');
    assert.ok(element.hasClass('test-class'), "component renders with class");
    assert.ok(!element.hasClass('active'), "component renders with class");
  });

  it('renders with active class name', function() {
    window.history.replaceState({}, '', '/test-server/something/');

    /* jshint ignore:start */
    testUtils.render(<Li className="test-class"
                         path="/test-server/something/" />);
    /* jshint ignore:end */

    let element = $('#test-mount li');
    assert.ok(element.hasClass('test-class'), "component renders with class");
    assert.ok(element.hasClass('active'), "component has active class");

    window.history.replaceState({}, '', '/test-server/something/else-deep/');

    /* jshint ignore:start */
    testUtils.render(<Li className="test-class"
                         path="/test-server/something/" />);
    /* jshint ignore:end */

    element = $('#test-mount li');
    assert.ok(element.hasClass('test-class'), "component renders with class");
    assert.ok(element.hasClass('active'), "component has active class");

    window.history.replaceState({}, '', '/test-server/');

    /* jshint ignore:start */
    testUtils.render(<Li className="test-class"
                         path="/test-server/something/" />);
    /* jshint ignore:end */

    element = $('#test-mount li');
    assert.ok(element.hasClass('test-class'), "component renders with class");
    assert.ok(!element.hasClass('active'), "component has no active class");
  });

  it('renders with custom active class', function() {
    window.history.replaceState({}, '', '/test-server/something/');

    /* jshint ignore:start */
    testUtils.render(<Li className="test-class"
                         path="/test-server/something/"
                         activeClassName="yay" />);
    /* jshint ignore:end */

    let element = $('#test-mount li');
    assert.ok(element.hasClass('test-class'), "component renders with class");
    assert.ok(!element.hasClass('active'), "component has no def active class");
    assert.ok(element.hasClass('yay'), "component has custom active class");

    window.history.replaceState({}, '', '/test-server/something/else-deep/');

    /* jshint ignore:start */
    testUtils.render(<Li className="test-class"
                         path="/test-server/something/"
                         activeClassName="yay" />);
    /* jshint ignore:end */

    element = $('#test-mount li');
    assert.ok(element.hasClass('test-class'), "component renders with class");
    assert.ok(!element.hasClass('active'), "component has no def active class");
    assert.ok(element.hasClass('yay'), "component has active class");

    window.history.replaceState({}, '', '/test-server/');

    /* jshint ignore:start */
    testUtils.render(<Li className="test-class"
                         path="/test-server/something/"
                         activeClassName="yay" />);
    /* jshint ignore:end */

    element = $('#test-mount li');
    assert.ok(element.hasClass('test-class'), "component renders with class");
    assert.ok(!element.hasClass('active'), "component has no def active class");
    assert.ok(!element.hasClass('yay'), "component has no active class");
  });
});
