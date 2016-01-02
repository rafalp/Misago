import React from 'react';
import { required } from 'misago/utils/validators';

export default class extends React.Component {
  validate() {
    let isValid = true;
    let errors = {};

    for (var key in this.state.validators) {
      if (this.state.validators.hasOwnProperty(key)) {
        let value = this.state[key];
        errors[key] = this.validateField(value, this.state.validators[key]);
        if (errors[key] !== null) {
          isValid = false;
        }
      }
    }

    return isValid ? null : errors;
  }

  validateField(value, validators) {
    let result = required()(value);
    let errors = [];

    if (result) {
      return [result];
    } else {
      for (let i in validators) {
        result = validators[i](value);
        if (result) {
          errors.push(result);
        }
      }
    }

    return errors.length ? errors : null;
  }

  changeValue(name, value) {
    let errors = null;
    if (this.state.validators.name) {
      errors = this.validateField(name, value);
    }
  }

  /* jshint ignore:start */
  bindInput = (name) => {
    return (event) => {
      let newState = {};
      newState[name] = event.target.value;
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
    event.preventDefault();

    if (this.state.isLoading) {
      return;
    }

    if (this.clean()) {
      this.setState({'isLoading': true});
      let promise = this.send();

      if (promise) {
        promise.then((success) => {
          this.handleSuccess(success);
          this.setState({'isLoading': false});
        }, (rejection) => {
          this.handleError(rejection);
          this.setState({'isLoading': false});
        });
      } else {
        this.setState({'isLoading': false});
      }
    }
  }
  /* jshint ignore:end */
}