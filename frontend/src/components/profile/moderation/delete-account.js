import React from 'react'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group'; // jshint ignore:line
import Loader from 'misago/components/modal-loader'; // jshint ignore:line
import ModalMessage from 'misago/components/modal-message'; // jshint ignore:line
import YesNoSwitch from 'misago/components/yes-no-switch'; // jshint ignore:line
import misago from 'misago/index'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import polls from 'misago/services/polls';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      isLoaded: false,
      isLoading: false,
      isDeleted: false,
      error: null,

      countdown: 5,
      confirm: false,

      with_content: false
    };
  }

  componentDidMount() {
    ajax.get(this.props.profile.api.delete).then(() => {
      this.setState({
        isLoaded: true
      });

      this.countdown();
    }, (rejection) => {
      this.setState({
        isLoaded: true,
        error: rejection.detail
      });
    });
  }

  /* jshint ignore:start */
  countdown = () => {
    window.setTimeout(() => {
      if (this.state.countdown > 1) {
        this.setState({
          countdown: this.state.countdown - 1,
        });
        this.countdown();
      } else if (!this.state.confirm) {
        this.setState({
          confirm: true
        });
      }
    }, 1000);
  };
  /* jshint ignore:end */

  send() {
    return ajax.post(this.props.profile.api.delete, {
      with_content: this.state.with_content
    });
  }

  handleSuccess() {
    polls.stop('user-profile');

    if (this.state.with_content) {
      this.setState({
        isDeleted: interpolate(gettext("%(username)s's account, threads, posts and other content has been deleted."), {
          'username': this.props.profile.username
        }, true)
      });
    } else {
      this.setState({
        isDeleted: interpolate(gettext("%(username)s's account has been deleted and other content has been hidden."), {
          'username': this.props.profile.username
        }, true)
      });
    }
  }

  getButtonLabel() {
    if (this.state.confirm) {
      return interpolate(gettext("Delete %(username)s"), {
        'username': this.props.profile.username
      }, true);
    } else {
      return interpolate(gettext("Please wait... (%(countdown)ss)"), {
        'countdown': this.state.countdown
      }, true);
    }
  }

  getForm() {
    /* jshint ignore:start */
    return <form onSubmit={this.handleSubmit}>
      <div className="modal-body">

        <FormGroup label={gettext("User content")}
                   for="id_with_content">
          <YesNoSwitch id="id_with_content"
                       disabled={this.state.isLoading}
                       labelOn={gettext("Delete together with user's account")}
                       labelOff={gettext("Hide after deleting user's account")}
                       onChange={this.bindInput('with_content')}
                       value={this.state.with_content} />
        </FormGroup>

      </div>
      <div className="modal-footer">

        <button type="button"
                className="btn btn-default"
                data-dismiss="modal">
          {gettext("Cancel")}
        </button>

        <Button className="btn-danger"
                loading={this.state.isLoading}
                disabled={!this.state.confirm}>
          {this.getButtonLabel()}
        </Button>

      </div>
    </form>;
    /* jshint ignore:end */
  }

  getDeletedBody() {
    /* jshint ignore:start */
    return <div className="modal-body">
      <div className="message-icon">
        <span className="material-icon">
          info_outline
        </span>
      </div>
      <div className="message-body">
        <p className="lead">
          {this.state.isDeleted}
        </p>
        <p>
          <a href={misago.get('USERS_LIST_URL')}>
            {gettext("Return to users list")}
          </a>
        </p>
      </div>
    </div>;
    /* jshint ignore:end */
  }

  getModalBody() {
    if (this.state.error) {
      /* jshint ignore:start */
      return <ModalMessage icon="remove_circle_outline"
                           message={this.state.error} />;
      /* jshint ignore:end */
    } else if (this.state.isLoaded) {
      if (this.state.isDeleted) {
        return this.getDeletedBody();
      } else {
        return this.getForm();
      }
    } else {
      /* jshint ignore:start */
      return <Loader />;
      /* jshint ignore:end */
    }
  }

  getClassName() {
    if (this.state.error || this.state.isDeleted) {
      return "modal-dialog modal-message modal-delete-account";
    } else {
      return "modal-dialog modal-delete-account";
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}
                role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal"
                  aria-label={gettext("Close")}>
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{gettext("Delete user account")}</h4>
        </div>
        {this.getModalBody()}
      </div>
    </div>;
    /* jshint ignore:end */
  }
}