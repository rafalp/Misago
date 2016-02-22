import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Search from 'misago/components/search'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Search Input", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    testUtils.render(<Search />);
    /* jshint ignore:end */

    let element = $('#test-mount .form-search');
    assert.ok(element.length, "element renders");

    assert.equal(element.find('input').attr('placeholder'), "Search...",
      "default placeholder is rendered");

    assert.equal(element.find('span').text(), 'search',
      "search icon is displayed");
  });

  it("renders with custom placeholder", function() {
    /* jshint ignore:start */
    testUtils.render(<Search placeholder="Search tests..." />);
    /* jshint ignore:end */

    let element = $('#test-mount .form-search');
    assert.ok(element.length, "element renders");

    assert.equal(element.find('input').attr('placeholder'), "Search tests...",
      "custom placeholder is rendered");

    assert.equal(element.find('span').text(), 'search',
      "search icon is displayed");
  });

  it("renders with custom class", function() {
    /* jshint ignore:start */
    testUtils.render(<Search className="extra-class" />);
    /* jshint ignore:end */

    let element = $('#test-mount .form-search');
    assert.ok(element.length, "element renders");
    assert.ok(element.hasClass('extra-class'), "element has extra class");
  });

  it("displays value", function() {
    /* jshint ignore:start */
    testUtils.render(<Search value="lorem ipsum" onChange={function() {}} />);
    /* jshint ignore:end */

    let element = $('#test-mount .form-control');
    assert.ok(element.length, "element renders");
    assert.equal(element.val(), "lorem ipsum", "element has value");
  });

  it("calls binding on change", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    let onChange = function(ev) {
      assert.equal(ev.target.value, 'BobBoberson', "callback was called");

      done();
    };

    testUtils.render(<Search onChange={onChange} />);
    /* jshint ignore:end */

    testUtils.simulateChange('#test-mount .form-control', 'BobBoberson');
  });
});