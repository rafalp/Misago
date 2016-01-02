import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import ReactTestUtils from 'react-addons-test-utils';
import Button from 'misago/components/button'; // jshint ignore:line

describe("Button", function() {
  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <Button>
        Lorem ipsum
      </Button>,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component rendered");
    assert.equal(element.attr('type'), 'submit', "component is submit button");
    assert.equal(element.text().trim(), "Lorem ipsum", "component contains child");
  });

  it('handles clicks', function(done) { // jshint ignore:line
    /* jshint ignore:start */
    function click() {
      assert.ok(true, "component called callback on click");
      done();
    }

    ReactDOM.render(
      <Button onClick={click}>
        Lorem ipsum
      </Button>,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component rendered");
    assert.equal(element.attr('type'), 'button', "component is regular button");
    ReactTestUtils.Simulate.click(element.get(0));
  });

  it('renders disabled', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <Button disabled={true}>
        Lorem ipsum
      </Button>,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component rendered");
    assert.equal(element.attr('disabled'), 'disabled', "component is disabled");
  });

  it('renders loading', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <Button loading={true}>
        Lorem ipsum
      </Button>,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount button>.loader-compact');
    assert.ok(element.length, "component rendered with loader");
    assert.equal(element.parent().attr('disabled'), 'disabled', "component is disabled");
  });
});
