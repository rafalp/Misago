import assert from 'assert';
import React from 'react'; // jshint ignore:line
import FormGroup from 'misago/components/form-group'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Form Group", function() {
  afterEach(function() {
    testUtils.emptyTestContainers();
  });

  it('renders', function() {
    /* jshint ignore:start */
    testUtils.render(
      <FormGroup label="Lorem Ipsum"
                 for="test_input">
        <input name="lorem" type="text" />
      </FormGroup>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .form-group');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('label').text().trim(), "Lorem Ipsum:",
      "input label is rendered");
    assert.equal(element.find('label').attr('for'), 'test_input',
      "input label for attribute is valid");

    assert.ok(element.find('input[name="lorem"]').length,
      "input field is rendered");
  });

  it('renders label and control classes', function() {
    /* jshint ignore:start */
    testUtils.render(
      <FormGroup label="Lorem Ipsum"
                 labelClass="test-label"
                 controlClass="test-control"
                 for="test_input">
        <input name="lorem" type="text" />
      </FormGroup>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .form-group');
    assert.ok(element.length, "component renders");

    assert.ok(element.find('label').hasClass('test-label'),
      "label has additional css class");
    assert.ok(element.find('div').hasClass('test-control'),
      "control has additional css class");
  });

  it('renders positive feedback', function() {
    /* jshint ignore:start */
    testUtils.render(
      <FormGroup label="Lorem Ipsum"
                 for="test_input"
                 validation={null}>
        <input name="lorem" type="text" />
      </FormGroup>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .form-group');
    assert.ok(element.length, "component renders");

    assert.ok(element.hasClass('has-feedback'), "has feedback");
    assert.ok(element.hasClass('has-success'), "has success");

    assert.ok(element.find('.form-control-feedback').text().trim(), 'check',
      "has feedback icon");
    assert.ok(element.find('#test_input_status').text().trim(), '(success)',
      "has feedback label for screen readers");
  });

  it('renders negative feedback', function() {
    /* jshint ignore:start */
    testUtils.render(
      <FormGroup label="Lorem Ipsum"
                 for="test_input"
                 validation={["First issue.", "Second issue."]}>
        <input name="lorem" type="text" />
      </FormGroup>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .form-group');
    assert.ok(element.length, "component renders");

    assert.ok(element.hasClass('has-feedback'), "has feedback");
    assert.ok(element.hasClass('has-error'), "has error");

    assert.ok(element.find('.form-control-feedback').text().trim(), 'clear',
      "has feedback icon");
    assert.ok(element.find('#test_input_status').text().trim(), '(error)',
      "has feedback label for screen readers");

    assert.ok(element.find('.help-block.errors p').length, 2,
      "errors list is rendered");

    assert.ok(element.find('.help-block.errors p').first().text().trim(),
      "First issue.",
      "first error is rendered");

    assert.ok(element.find('.help-block.errors p').last().text().trim(),
      "Second issue.",
      "second error is rendered");
  });

  it('renders help text', function() {
    /* jshint ignore:start */
    testUtils.render(
      <FormGroup label="Lorem Ipsum"
                 for="test_input"
                 helpText="Lorem ipsum dolor met.">
        <input name="lorem" type="text" />
      </FormGroup>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .form-group');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('p.help-block').text().trim(),
      "Lorem ipsum dolor met.",
      "help text renders");
  });

  it('renders extra', function() {
    /* jshint ignore:start */
    testUtils.render(
      <FormGroup label="Lorem Ipsum"
                 for="test_input"
                 extra={<p id="row-extra">Extra!!!</p>}>
        <input name="lorem" type="text" />
      </FormGroup>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .form-group');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('#row-extra').text().trim(), "Extra!!!",
      "extra component was rendered");
  });
});
