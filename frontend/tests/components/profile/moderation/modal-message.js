import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ModalMessage from 'misago/components/profile/moderation/modal-message'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("User Profile Moderation Modal Message", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    testUtils.render(<ModalMessage message="Lorem ipsum dolor met elit." />);
    /* jshint ignore:end */

    let element = $('#test-mount .modal-body');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('.material-icon').text(), 'remove_circle_outline',
      "component renders default icon");

    assert.equal(element.find('p.lead').text(), "Lorem ipsum dolor met elit.",
      "component renders specified message");
  });

  it("renders custom icon", function() {
    /* jshint ignore:start */
    testUtils.render(
      <ModalMessage message="Lorem ipsum dolor met elit."
                    icon="custom_icon" />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .modal-body');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('.material-icon').text(), 'custom_icon',
      "component renders custom icon");

    assert.equal(element.find('p.lead').text(), "Lorem ipsum dolor met elit.",
      "component renders specified message");
  });
});