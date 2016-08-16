import React from 'react'; //jshint ignore:line
import Editor from 'misago/components/editor'; //jshint ignore:line
import Form from 'misago/components/form';
import Container from './utils/container'; //jshint ignore:line
import Loader from './utils/loader'; //jshint ignore:line
import Message from './utils/message'; //jshint ignore:line
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

      validators: {
        post: getPostValidators()
      },
      errors: {}
    };
  }

  componentDidMount() {
    ajax.get(this.props.config, this.props.context || null).then(this.loadSuccess, this.loadError);
  }

  /* jshint ignore:start */
  loadSuccess = (data) => {
    this.setState({
      isReady: true,

      post: '' || '[quote]\n' + data.post + '\n[/quote]'
    });
  };

  loadError = (rejection) => {
    this.setState({
      isErrored: rejection.detail
    });
  };

  onCancel = () => {
    const cancel = confirm(gettext("Are you sure you want to discard your reply?"));
    if (cancel) {
      posting.close();
    }
  };

  onPostchange = (event) => {
    this.changeValue('post', event.target.value);
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
      post: this.state.post
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
                  loading={this.state.isLoading}
                  onCancel={this.onCancel}
                  onChange={this.onPostchange}
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
