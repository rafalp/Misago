import assert from 'assert';
import React from 'react'; // jshint ignore:line
import PanelMessage from 'misago/components/panel-message'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Panel Message", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    testUtils.render(<PanelMessage message="Lorem ipsum dolor met!" />);
    /* jshint ignore:end */

    let element = $('#test-mount .panel-body');
    assert.ok(element.length, "component renders");
    assert.equal(element.find('.material-icon').text(), 'info_outline',
      "has default icon");
    assert.equal(element.find('p.lead').text(), "Lorem ipsum dolor met!",
      "has specified message");
  });

  it("renders with custom icon", function() {
    /* jshint ignore:start */
    testUtils.render(
      <PanelMessage icon="other_icon"
                    message="Lorem ipsum dolor met!" />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .panel-body');
    assert.ok(element.length, "component renders");
    assert.equal(element.find('.material-icon').text(), 'other_icon',
      "has default icon");
    assert.equal(element.find('p.lead').text(), "Lorem ipsum dolor met!",
      "has specified message");
  });

  it("renders with help text", function() {
    /* jshint ignore:start */
    testUtils.render(
      <PanelMessage icon="other_icon"
                    message="Lorem ipsum dolor met!"
                    helpText="This is help text." />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .panel-body');
    assert.ok(element.length, "component renders");
    assert.equal(element.find('.material-icon').text(), 'other_icon',
      "has default icon");
    assert.equal(element.find('p.lead').text(), "Lorem ipsum dolor met!",
      "has specified message");
    assert.equal(element.find('p.help-block').text(), "This is help text.",
      "has specified help text");
  });
});
