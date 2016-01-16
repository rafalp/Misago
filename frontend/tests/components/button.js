import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Button", function() {
  afterEach(function() {
    testUtils.emptyTestContainers();
  });

  it('renders', function() {
    /* jshint ignore:start */
    testUtils.render(<Button>Lorem ipsum</Button>);
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component rendered");
    assert.equal(element.attr('type'), 'submit', "component is submit button");
    assert.equal(element.text().trim(), "Lorem ipsum",
      "component contains child");
  });

  it('handles clicks', function(done) { // jshint ignore:line
    /* jshint ignore:start */
    function click() {
      assert.ok(true, "component called callback on click");
      done();
    }

    testUtils.render(<Button onClick={click}>Lorem ipsum</Button>);
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component rendered");
    assert.equal(element.attr('type'), 'button', "component is regular button");
    testUtils.simulateClick('#test-mount button');
  });

  it('renders disabled', function() {
    /* jshint ignore:start */
    testUtils.render(<Button disabled={true}>Lorem ipsum</Button>);
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component rendered");
    assert.equal(element.attr('disabled'), 'disabled', "component is disabled");
  });

  it('renders loading', function() {
    /* jshint ignore:start */
    testUtils.render(<Button loading={true}>Lorem ipsum</Button>);
    /* jshint ignore:end */

    let element = $('#test-mount button>.loader');
    assert.ok(element.length, "component rendered with loader");
    assert.equal(element.parent().attr('disabled'), 'disabled',
      "component is disabled");
  });
});
