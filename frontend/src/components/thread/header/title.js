import React from 'react'; //jshint ignore:line
import Form from 'misago/components/form';
import { getTitleValidators } from 'misago/components/posting/utils/validators';
import * as thread from 'misago/reducers/thread';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      isEditing: false,
      isLoading: false,

      title: props.thread.title,

      validators: {
        title: getTitleValidators()
      },
      errors: {}
    };
  }

  /* jshint ignore:start */
  onChange = (event) => {
    this.changeValue('title', event.target.value);
  };

  onEdit = () => {
    this.setState({
      isEditing: true
    });
  };

  onCancel = () => {
    this.setState({
      title: this.props.thread.title,

      isEditing: false
    });
  };
  /* jshint ignore:end */

  clean() {
    if (!this.state.title.trim().length) {
      snackbar.error(gettext("You have to enter thread title."));
      return false;
    }

    const errors = this.validate();

    if (errors.title) {
      snackbar.error(errors.title[0]);
      return false;
    }

    return true;
  }

  send() {
    return ajax.patch(this.props.thread.api.index, [
      {op: 'replace', path: 'title', value: this.state.title}
    ]);
  }

  handleSuccess(data) {
    store.dispatch(thread.update(data));

    this.setState({
      'isEditing': false
    });
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      console.log(rejection);
    } else {
      snackbar.apiError(rejection);
    }
  }

  render() {
    /* jshint ignore:start */
    if (this.state.isEditing) {
      return (
        <form onSubmit={this.handleSubmit} className="pull-left title-edit-form">
          <input className="form-control" type="text" value={this.state.title} onChange={this.onChange} />
          <button
            className="btn btn-default"
            disabled={this.state.isLoading}
            title={gettext("Change title")}
          >
            <span className="material-icon">check_circle</span>
          </button>
          <button
            className="btn btn-default"
            disabled={this.state.isLoading}
            onClick={this.onCancel}
            title={gettext("Cancel")}
            type="button"
          >
            <span className="material-icon">cancel</span>
          </button>
        </form>
      );
    } else if (this.props.user.id && this.props.thread.acl.can_edit) {
      return (
        <div className="pull-left title-editable">
          <h1>
            {this.props.thread.title}
          </h1>
          <button
            className="btn btn-default"
            onClick={this.onEdit}
            title={gettext("Edit title")}
            type="button"
          >
            <span className="material-icon">edit</span>
          </button>
        </div>
      );
    } else {
      return (
        <div className="pull-left">
          <h1>{this.props.thread.title}</h1>
        </div>
      );
    }
    /* jshint ignore:end */
  }
}
