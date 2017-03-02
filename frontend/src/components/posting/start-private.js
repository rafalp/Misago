import React from 'react'; //jshint ignore:line
import Editor from 'misago/components/editor'; //jshint ignore:line
import Form from 'misago/components/form';
import Container from './utils/container'; //jshint ignore:line
import Message from './utils/message'; //jshint ignore:line
import * as attachments from './utils/attachments'; //jshint ignore:line
import cleanUsernames from './utils/usernames'; //jshint ignore:line
import { getPostValidators, getTitleValidators } from './utils/validators';
import ajax from 'misago/services/ajax';
import posting from 'misago/services/posting'; //jshint ignore:line
import snackbar from 'misago/services/snackbar';

export default class extends Form {
  constructor(props) {
    super(props);

    const to = (props.to || []).map((user) => user.username).join(', ');

    this.state = {
      isLoading: false,

      to: to,
      title: '',
      post: '',
      attachments: [],

      validators: {
        title: getTitleValidators(),
        post: getPostValidators()
      },
      errors: {}
    };
  }

  /* jshint ignore:start */
  onCancel = () => {
    const cancel = confirm(gettext("Are you sure you want to discard private thread?"));
    if (cancel) {
      posting.close();
    }
  };

  onToChange = (event) => {
    this.changeValue('to', event.target.value);
  };

  onTitleChange = (event) => {
    this.changeValue('title', event.target.value);
  };

  onPostChange = (event) => {
    this.changeValue('post', event.target.value);
  };

  onAttachmentsChange = (attachments) => {
    this.setState({
      attachments
    });
  };
  /* jshint ignore:end */

  clean() {
    if (!cleanUsernames(this.state.to).length) {
      snackbar.error(gettext("You have to enter at least one recipient."));
      return false;
    }

    if (!this.state.title.trim().length) {
      snackbar.error(gettext("You have to enter thread title."));
      return false;
    }

    if (!this.state.post.trim().length) {
      snackbar.error(gettext("You have to enter a message."));
      return false;
    }

    const errors = this.validate();

    if (errors.title) {
      snackbar.error(errors.title[0]);
      return false;
    }

    if (errors.post) {
      snackbar.error(errors.post[0]);
      return false;
    }

    return true;
  }

  send() {
    return ajax.post(this.props.submit, {
      to: cleanUsernames(this.state.to),
      title: this.state.title,
      post: this.state.post,
      attachments: attachments.clean(this.state.attachments),
    });
  }

  handleSuccess(success) {
    snackbar.success(gettext("Your thread has been posted."));
    window.location = success.url;

    // keep form loading
    this.setState({
      'isLoading': true
    });
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      const errors = [].concat(
        rejection.non_field_errors || [],
        rejection.to || [],
        rejection.title || [],
        rejection.post || []
      );

      snackbar.error(errors[0]);
    } else {
      snackbar.apiError(rejection);
    }
  }

  render() {
    /* jshint ignore:start */
    return (
      <Container className="posting-form" withFirstRow={true}>
        <form onSubmit={this.handleSubmit}>
          <div className="row first-row">
            <div className="col-xs-12">

              <input
                className="form-control"
                disabled={this.state.isLoading}
                onChange={this.onToChange}
                placeholder={gettext("Comma separated list of user names, eg.: Danny, Lisa")}
                type="text"
                value={this.state.to}
              />

            </div>
          </div>
          <div className="row first-row">
            <div className="col-xs-12">

              <input
                className="form-control"
                disabled={this.state.isLoading}
                onChange={this.onTitleChange}
                placeholder={gettext("Thread title")}
                type="text"
                value={this.state.title}
              />

            </div>
          </div>
          <div className="row">
            <div className="col-xs-12">

              <Editor
                attachments={this.state.attachments}
                loading={this.state.isLoading}
                onAttachmentsChange={this.onAttachmentsChange}
                onCancel={this.onCancel}
                onChange={this.onPostChange}
                submitLabel={gettext("Post thread")}
                value={this.state.post}
              />

            </div>
          </div>
        </form>
      </Container>
    );
    /* jshint ignore:end */
  }
}
