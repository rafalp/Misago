import React from 'react'; //jshint ignore:line
import Editor from 'misago/components/editor'; //jshint ignore:line
import Form from 'misago/components/form';
import Container from './utils/container'; //jshint ignore:line
import Loader from './utils/loader'; //jshint ignore:line
import Message from './utils/message'; //jshint ignore:line
import * as attachments from './utils/attachments'; //jshint ignore:line
import { getPostValidators } from './utils/validators';
import ajax from 'misago/services/ajax';
import posting from 'misago/services/posting'; //jshint ignore:line
import snackbar from 'misago/services/snackbar';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      isReady: false,
      isLoading: false,
      isErrored: false,

      post: '',
      attachments: [],

      validators: {
        post: getPostValidators()
      },
      errors: {}
    };
  }

  componentDidMount() {
    ajax.get(this.props.config, this.props.context || null).then(this.loadSuccess, this.loadError);
  }

  componentWillReceiveProps(nextProps) {
    const context = this.props.context;
    const newContext = nextProps.context;

    if (context && newContext && context.reply === newContext.reply) return;

    ajax.get(nextProps.config, nextProps.context || null).then(this.appendData, snackbar.apiError);
  }

  /* jshint ignore:start */
  loadSuccess = (data) => {
    this.setState({
      isReady: true,

      post: data.post ? ('[quote="@' +  data.poster + '"]\n' + data.post + '\n[/quote]') : ''
    });
  };

  loadError = (rejection) => {
    this.setState({
      isErrored: rejection.detail
    });
  };

  appendData = (data) => {
    const newPost = data.post ? ('[quote="@' +  data.poster + '"]\n' + data.post + '\n[/quote]\n\n') : '';

    this.setState((prevState, props) => {
      if (prevState.post.length > 0) {
        return {
          post: prevState.post + '\n\n' + newPost
        };
      }

      return {
        post: newPost
      };
    });
  };

  onCancel = () => {
    const cancel = confirm(gettext("Are you sure you want to discard your reply?"));
    if (cancel) {
      posting.close();
    }
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
    if (!this.state.post.trim().length) {
      snackbar.error(gettext("You have to enter a message."));
      return false;
    }

    const errors = this.validate();

    if (errors.post) {
      snackbar.error(errors.post[0]);
      return false;
    }

    return true;
  }

  send() {
    return ajax.post(this.props.submit, {
      post: this.state.post,
      attachments: attachments.clean(this.state.attachments)
    });
  }

  handleSuccess(success) {
    snackbar.success(gettext("Your reply has been posted."));
    window.location = success.url.index;

    // keep form loading
    this.setState({
      'isLoading': true
    });
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      if (rejection.category) {
        snackbar.error(rejection.category[0]);
      } else if (rejection.title) {
        snackbar.error(rejection.title[0]);
      } else if (rejection.post) {
        snackbar.error(rejection.post[0]);
      }
    } else {
      snackbar.apiError(rejection);
    }
  }

  render() {
    /* jshint ignore:start */
    if (this.state.isReady) {
      return (
        <Container className="posting-form">
          <form onSubmit={this.handleSubmit} method="POST">
            <div className="row">
              <div className="col-md-12">

                <Editor
                  attachments={this.state.attachments}
                  loading={this.state.isLoading}
                  onAttachmentsChange={this.onAttachmentsChange}
                  onCancel={this.onCancel}
                  onChange={this.onPostChange}
                  submitLabel={gettext("Post reply")}
                  value={this.state.post}
                />

              </div>
            </div>
          </form>
        </Container>
      );
    } else if (this.state.isErrored) {
      return (
        <Message message={this.state.isErrored} />
      );
    } else {
      return (
        <Loader />
      );
    }
    /* jshint ignore:end */
  }
}
