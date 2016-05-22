import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ErrorsList from 'misago/components/threads/moderation/errors-list'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Threads List Moderation Errors List", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    const errors = [
      {
        thread: {
          id: 123,
          title: "Lorem ipsum dolor met"
        },
        errors: [
          "Requested thread could not be found."
        ]
      },
      {
        thread: {
          id: 124,
          title: "Test thread"
        },
        errors: [
          "You don't have permission to pin this thread.",
          "You don't have permission to close this thread."
        ]
      }
    ];

    /* jshint ignore:start */
    testUtils.render(<ErrorsList errors={errors} />);
    /* jshint ignore:end */

    const element = $('#test-mount .modal-dialog');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('.list-item-errors').length, 2,
      "two threads errors lists are displayed");

    const errorsList = element.find('.list-item-errors li');
    assert.equal(errorsList.length, 3, "three errors are displayed");
    assert.equal(errorsList.eq(0).text(), errors[0].errors[0],
      "valid error is displayed");
    assert.equal(errorsList.eq(1).text(), errors[1].errors[0],
      "valid error is displayed");
    assert.equal(errorsList.eq(2).text(), errors[1].errors[1],
      "valid error is displayed");
  });
});
