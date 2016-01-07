import React from 'react';
import { required } from 'misago/utils/validators';

let validateRequired = required();

export default class extends React.Component {
  validate() {
    let errors = {};

    let validators = {
      required: this.state.validators.required || this.state.validators,
      optional: this.state.validators.optional || {}
    };

    let validatedFields = [];

    // add required fields to validation
    for (let name in validators.required) {
      if (validators.required.hasOwnProperty(name) &&
          validators.required[name]) {
        validatedFields.push(name);
      }
    }

    // add optional fields to validation
    for (let name in validators.optional) {
      if (validators.optional.hasOwnProperty(name) &&
          validators.optional[name]) {
        validatedFields.push(name);
      }
    }

    // validate fields values
    for (let i in validatedFields) {
      let name = validatedFields[i];
      let fieldErrors = this.validateField(name, this.state[name]);

      if (fieldErrors === null) {
        errors[name] = null;
      } else if (fieldErrors) {
        errors[name] = fieldErrors;
      }
    }

    return errors;
  }

  isValid() {
    let errors = this.validate();
    for (let field in errors) {
      if (errors.hasOwnProperty(field)) {
        if (errors[field] !== null) {
          return false;
        }
      }
    }

    return true;
  }

  validateField(name, value) {
    let errors = [];

    let validators = {
      required: (this.state.validators.required || this.state.validators)[name],
      optional: (this.state.validators.optional || {})[name]
    };

    let requiredError = validateRequired(value) || false;

    if (validators.required) {
      if (requiredError) {
        errors = [requiredError];
      } else {
        for (let i in validators.required) {
          let validationError = validators.required[i](value);
          if (validationError) {
            errors.push(validationError);
          }
        }
      }

      return errors.length ? errors : null;
    } else if (requiredError === false && validators.optional) {
      for (let i in validators.optional) {
        let validationError = validators.optional[i](value);
        if (validationError) {
          errors.push(validationError);
        }
      }

      return errors.length ? errors : null;
    }

    return false; // false === field wasn't validated
  }

  /* jshint ignore:start */
  bindInput = (name) => {
    return (event) => {
      let newState = {};
      newState[name] = event.target.value;

      let formErrors = this.state.errors || {};
      formErrors[name] = this.validateField(name, newState[name]);
      newState.errors = formErrors;

      this.setState(newState);
    }
  }

  clean() {
    return true;
  }

  send() {
    return null;
  }

  handleSuccess(success) {
    return;
  }

  handleError(rejection) {
    return;
  }

  handleSubmit = (event) => {
    // we don't reload page on submissions
    event.preventDefault()
    if (this.state.isLoading) {
      return;
    }

    if (this.clean()) {
      this.setState({'isLoading': true});
      let promise = this.send();

      if (promise) {
        promise.then((success) => {
          this.setState({'isLoading': false});
          this.handleSuccess(success);
        }, (rejection) => {
          this.setState({'isLoading': false});
          this.handleError(rejection);
        });
      } else {
        this.setState({'isLoading': false});
      }
    }
  }
  /* jshint ignore:end */
}