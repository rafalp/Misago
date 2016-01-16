import assert from 'assert';
import React from 'react'; // jshint ignore:line
import Form from 'misago/components/form';
import { email, minLength } from 'misago/utils/validators'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

var form = null;

class TestForm extends Form { // jshint ignore:line
  constructor(props) {
    super(props);

    this.state = {
      'isLoading': false,

      'requiredField': '',
      'validatedField': '',
      'optionalField': '',

      validators: {
        required: {
          'requiredField': [],
          'validatedField': [email("That ain't valid e-mail!")]
        },
        optional: {
          'optionalField': [minLength(4)]
        }
      }
    };
  }

  render() {
    /* jshint ignore:start */
    return <p>No need</p>;
    /* jshint ignore:end */
  }
}

describe("Form", function() {
  beforeEach(function() {
    /* jshint ignore:start */
    form = testUtils.render(<TestForm />, 'test-mount');
    /* jshint ignore:end */
  });

  afterEach(function() {
    testUtils.emptyTestContainers();
  });

  it("validates individual field", function() {
    assert.deepEqual(
      form.validateField('requiredField', ''), ["This field is required."],
      "empty value returned error");
    assert.equal(form.validateField('requiredField', 'required'), null,
      "non-empty value returned no errors");

    assert.deepEqual(
      form.validateField('validatedField', 'lorem'),
      ["That ain't valid e-mail!"],
      "invalid value returned error from validator");
    assert.deepEqual(
      form.validateField('validatedField', 'lorem@ipsum.com'), null,
      "valid value returned no errors from validation");
  });

  it("yields errors on empty fields", function(done) {
    form.forceUpdate(function() {
      assert.deepEqual(form.validate(), {
        'requiredField': ["This field is required."],
        'validatedField': ["This field is required."]
      }, "both required inputs failed to pass initial validation");

      done();
    });
  });

  it("yields errors on invalid fields", function(done) {
    form.setState({
      'requiredField': "Its okay!",
      'validatedField': "Lorem ipsumd dolor met."
    });

    form.forceUpdate(function() {
      assert.deepEqual(form.validate(), {
        'requiredField': null,
        'validatedField': ["That ain't valid e-mail!"]
      }, "invalid field failed to pass validation");

      done();
    });
  });

  it("yields errors on invalid optional fields", function(done) {
    form.setState({
      'requiredField': "Its okay!",
      'validatedField': "Lorem ipsumd dolor met.",
      'optionalField': "sho"
    });

    form.forceUpdate(function() {
      assert.deepEqual(form.validate(), {
        'requiredField': null,
        'validatedField': ["That ain't valid e-mail!"],
        'optionalField': [
          "Ensure this value has at least 4 characters (it has 3)."
        ]
      }, "invalid optional field failed to pass validation");

      done();
    });
  });

  it("passes valid form", function(done) {
    form.setState({
      'requiredField': "Its okay!",
      'validatedField': "lorem@ipsum.com",
      'optionalField': "Lorem ipsum dolor long!"
    });

    form.forceUpdate(function() {
      assert.deepEqual(form.validate(), {
        'requiredField': null,
        'validatedField': null,
        'optionalField': null
      }, "valid fields passed validation");

      done();
    });
  });

  it("binds fields", function(done) {
    form.bindInput('requiredField')({target: {value: "It's okay!"}});
    form.bindInput('validatedField')({target: {value: "Not a e-mail!"}});

    form.forceUpdate(function() {
      assert.deepEqual(form.state.errors, {
        'requiredField': null,
        'validatedField': ["That ain't valid e-mail!"]
      }, "invalid field failed to pass validation");

      done();
    });
  });
});