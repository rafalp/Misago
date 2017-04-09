/* jshint ignore:start */
import React from 'react';
import Breadcrumbs from './breadcrumbs';
import { isModerationVisible, ModerationControls } from '../moderation/thread';
import Stats from './stats';
import Form from 'misago/components/form';
import { getTitleValidators } from 'misago/components/posting/utils/validators';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as thread from 'misago/reducers/thread';

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
    const {thread, user} = this.props;
    const showModeration = user.id && isModerationVisible(thread);

    if (this.state.isEditing) {
      return (
        <div className="page-header with-stats with-breadcrumbs">
          <Breadcrumbs path={thread.path} />
          <div className="container">
            <div className="row xs-margin-top sm-margin-top title-edit-form">
              <form onSubmit={this.handleSubmit}>
                <div className="col-sm-6 col-md-6">
                  <input
                    className="form-control"
                    type="text"
                    value={this.state.title}
                    onChange={this.onChange}
                  />
                </div>
                <div className="col-sm-6 col-md-4">
                  <div className="row xs-margin-top-half sm-margin-top-no md-margin-top-no">
                    <div className="col-xs-6">
                      <button
                        className="btn btn-success btn-block btn-outline"
                        disabled={this.state.isLoading}
                        title={gettext("Change title")}
                      >
                        {gettext("Save changes")}
                      </button>
                    </div>
                    <div className="col-xs-6">
                      <button
                        className="btn btn-default btn-block btn-outline"
                        disabled={this.state.isLoading}
                        onClick={this.onCancel}
                        title={gettext("Cancel")}
                        type="button"
                      >
                        {gettext("Cancel")}
                      </button>
                    </div>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <Stats thread={thread} />
        </div>
      );
    } else if (user.id && thread.acl.can_edit) {
      return (
        <div className="page-header with-stats with-breadcrumbs">
          <Breadcrumbs path={thread.path} />
          <div className="container">
            <div className="row">
              <div className={showModeration ? "col-sm-9 col-md-8" : "col-sm-10 col-md-10"}>
                <h1>
                  {thread.title}
                </h1>
              </div>
              <div className={showModeration ? "col-sm-3 col-md-4" : "col-sm-3 col-md-2"}>
                <div className="row xs-margin-top sm-margin-top md-margin-top-no">
                  <div className="col-xs-6">
                    <button
                      className="btn btn-default btn-block btn-outline"
                      onClick={this.onEdit}
                      title={gettext("Edit title")}
                      type="button"
                    >
                      <span className="material-icon">edit</span>
                      <span className="hidden-sm">
                        {gettext("Edit")}
                      </span>
                    </button>
                  </div>
                  {showModeration && (
                    <Moderation {...this.props} />
                  )}
                </div>
              </div>
            </div>
          </div>
          <Stats thread={thread} />
        </div>
      );
    } else if (showModeration) {
      return (
        <div className="page-header with-stats with-breadcrumbs">
          <Breadcrumbs path={thread.path} />
          <div className="container">
            <div className="row">
              <div className="col-sm-9 col-md-10">
                <h1>
                  {thread.title}
                </h1>
              </div>
              <div className="col-sm-3 col-md-2">
                <div className="row xs-margin-top sm-margin-top md-margin-top-no">
                  <Moderation
                    isSingle={true}
                    {...this.props}
                  />
                </div>
              </div>
            </div>
          </div>
          <Stats thread={thread} />
        </div>
      );
    }

    return (
      <div className="page-header with-stats with-breadcrumbs">
        <Breadcrumbs path={thread.path} />
        <div className="container">
          <h1>{thread.title}</h1>
        </div>
        <Stats thread={thread} />
      </div>
    );
  }
}

export function Moderation(props) {
  return (
    <div className={props.isSingle ? "col-xs-12" : "col-xs-6"}>
      <div className="btn-group btn-group-justified">
        <div className="btn-group">
          <button
            aria-expanded="false"
            aria-haspopup="true"
            className="btn btn-default btn-outline dropdown-toggle"
            data-toggle="dropdown"
            disabled={props.thread.isBusy}
            type="button"
          >
            <span className="material-icon">
              settings
            </span>
            <span className={props.isSingle ? "" : "hidden-sm"}>
              {gettext("Moderation")}
            </span>
          </button>
          <ModerationControls
            posts={props.posts}
            thread={props.thread}
            user={props.user}
          />
        </div>
      </div>
    </div>
  );
}