import React from 'react';

export default class extends React.Component {
  isValidated() {
    return typeof this.props.validation !== "undefined";
  }

  getClassName() {
    let className = 'form-group';
    if (this.isValidated()) {
      className += ' has-feedback';
      if (this.props.validation === null) {
        className += ' has-success';
      } else {
        className += ' has-error';
      }
    }
    return className;
  }

  getFeedback() {
    if (this.props.validation) {
      /* jshint ignore:start */
      return <div className="help-block errors">
        {this.props.validation.map((error, i) => {
          return <p key={this.props.for + 'FeedbackItem' + i}>{error}</p>;
        })}
      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getFeedbackIcon() {
    if (this.isValidated()) {
      /* jshint ignore:start */
      return <span className="material-icon form-control-feedback"
                   aria-hidden="true" key={this.props.for + 'FeedbackIcon'}>
        {this.props.validation ? 'clear' : 'check'}
      </span>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getFeedbackDescription() {
    if (this.isValidated()) {
      /* jshint ignore:start */
      return <span id={this.props.for + '_status'} className="sr-only">
        {this.props.validation ? gettext('(error)') : gettext('(success)')}
      </span>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getHelpText() {
    if (this.props.helpText) {
      /* jshint ignore:start */
      return <p className="help-block">{this.props.helpText}</p>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>
      <label className={'control-label ' + (this.props.labelClass || '')}
             htmlFor={this.props.for || ''}>
        {this.props.label}:
      </label>
      <div className={this.props.controlClass || ''}>
        {this.props.children}
        {this.getFeedbackIcon()}
        {this.getFeedbackDescription()}
        {this.getFeedback()}
        {this.getHelpText()}
        {this.props.extra || null}
      </div>
    </div>
    /* jshint ignore:end */
  }
}
