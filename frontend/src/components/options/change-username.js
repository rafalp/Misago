import moment from 'moment';
import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group'; // jshint ignore:line
import Loader from 'misago/components/loader'; // jshint ignore:line
import misago from 'misago/index';
import { dehydrate, addNameChange } from 'misago/reducers/username-history'; // jshint ignore:line
import { updateUsername } from 'misago/reducers/users'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import title from 'misago/services/page-title';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as random from 'misago/utils/random'; // jshint ignore:line
import * as validators from 'misago/utils/validators';

export class ChangeUsername extends Form {
  constructor(props) {
    super(props);

    this.state = {
      username: '',

      validators: {
        username: [
          validators.usernameContent(),
          validators.usernameMinLength({
            username_length_min: props.options.length_min
          }),
          validators.usernameMaxLength({
            username_length_max: props.options.length_max
          })
        ]
      },

      isLoading: false
    };
  }

  getHelpText() {
    let phrases = [];

    if (this.props.options.changes_left > 0) {
      let message = ngettext(
        "You can change your username %(changes_left)s more time.",
        "You can change your username %(changes_left)s more times.",
        this.props.options.changes_left);

      phrases.push(interpolate(message, {
        'changes_left': this.props.options.changes_left
      }, true));
    }

    if (this.props.user.acl.name_changes_expire > 0) {
      let message = ngettext(
        "Used changes redeem after %(name_changes_expire)s day.",
        "Used changes redeem after %(name_changes_expire)s days.",
        this.props.user.acl.name_changes_expire);

      phrases.push(interpolate(message, {
        'name_changes_expire': this.props.user.acl.name_changes_expire
      }, true));
    }

    return phrases.length ? phrases.join(' ') : null;
  }

  clean() {
    let errors = this.validate();
    if (errors.username) {
      snackbar.error(errors.username[0]);
      return false;
    } if (this.state.username.trim() === this.props.user.username) {
      snackbar.info(gettext("Your new username is same as current one."));
      return false;
    } else {
      return true;
    }
  }

  send() {
    return ajax.post(this.props.user.api_url.username, {
      'username': this.state.username
    });
  }

  handleSuccess(success) {
    this.setState({
      'username': ''
    });

    this.props.complete(success.username, success.slug, success.options);
  }

  handleError(rejection) {
    snackbar.apiError(rejection);
  }

  render() {
    /* jshint ignore:start */
    return <form onSubmit={this.handleSubmit} className="form-horizontal">
      <div className="panel panel-default panel-form">
        <div className="panel-heading">
          <h3 className="panel-title">{gettext("Change username")}</h3>
        </div>
        <div className="panel-body">

          <FormGroup label={gettext("New username")} for="id_username"
                     labelClass="col-sm-4" controlClass="col-sm-8"
                     helpText={this.getHelpText()}>
            <input type="text" id="id_username" className="form-control"
                   disabled={this.state.isLoading}
                   onChange={this.bindInput('username')}
                   value={this.state.username} />
          </FormGroup>

        </div>
        <div className="panel-footer">
          <div className="row">
            <div className="col-sm-8 col-sm-offset-4">

              <Button className="btn-primary" loading={this.state.isLoading}>
                {gettext("Change username")}
              </Button>

            </div>
          </div>
        </div>
      </div>
    </form>;
    /* jshint ignore:end */
  }
}

export class NoChangesLeft extends React.Component {
  getHelpText() {
    if (this.props.options.next_on) {
      return interpolate(
          gettext("You will be able to change your username %(next_change)s."),
          {'next_change': this.props.options.next_on.fromNow()}, true);
    } else {
      return gettext("You have used up available name changes.");
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="panel panel-default panel-form">
      <div className="panel-heading">
        <h3 className="panel-title">{gettext("Change username")}</h3>
      </div>
      <div className="panel-body panel-message-body">

        <div className="message-icon">
          <span className="material-icon">
            info_outline
          </span>
        </div>
        <div className="message-body">
          <p className="lead">
            {gettext("You can't change your username at the moment.")}
          </p>
          <p className="help-block">
            {this.getHelpText()}
          </p>
        </div>

      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export class ChangeUsernameLoading extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="panel panel-default panel-form">
      <div className="panel-heading">
        <h3 className="panel-title">{gettext("Change username")}</h3>
      </div>
      <div className="panel-body panel-body-loading">

        <Loader className="loader loader-spaced" />

      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export class UsernameHistory extends React.Component {
  renderUserAvatar(item) {
    if (item.changed_by) {
      /* jshint ignore:start */
      return <a href={item.changed_by.absolute_url} className="user-avatar">
        <Avatar user={item.changed_by} size="100" />
      </a>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <span className="user-avatar">
        <Avatar size="100" />
      </span>;
      /* jshint ignore:end */
    }
  }

  renderUsername(item) {
    if (item.changed_by) {
      /* jshint ignore:start */
      return <a href={item.changed_by.absolute_url} className="item-title">
        {item.changed_by.username}
      </a>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <span className="item-title">
        {item.changed_by_username}
      </span>;
      /* jshint ignore:end */
    }
  }

  renderHistory() {
    /* jshint ignore:start */
    return <div className="username-history ui-ready">
      <ul className="list-group">
        {this.props.changes.map((item) => {
          return <li className="list-group-item" key={item.id}>
            <div className="username-change-avatar">
              {this.renderUserAvatar(item)}
            </div>
            <div className="username-change-author">
              {this.renderUsername(item)}
            </div>
            <div className="username-change">
              {item.old_username}
              <span className="material-icon">
                arrow_forward
              </span>
              {item.new_username}
            </div>
            <div className="username-change-date">
              <abbr title={item.changed_on.format('LLL')}>
                {item.changed_on.fromNow()}
              </abbr>
            </div>
          </li>;
        })}
      </ul>
    </div>;
    /* jshint ignore:end */
  }

  renderEmptyHistory() {
    /* jshint ignore:start */
    return <div className="username-history ui-ready">
      <ul className="list-group">
        <li className="list-group-item empty-message">
          {gettext("No name changes have been recorded for your account.")}
        </li>
      </ul>
    </div>;
    /* jshint ignore:end */
  }

  renderHistoryPreview() {
    /* jshint ignore:start */
    return <div className="username-history ui-preview">
      <ul className="list-group">
        {random.range(3, 5).map((i) => {
          return <li className="list-group-item" key={i}>
            <div className="username-change-avatar">
              <span className="user-avatar">
                <Avatar size="100" />
              </span>
            </div>
            <div className="username-change-author">
              <span className="ui-preview-text" style={{width: random.int(30, 100) + "px"}}>&nbsp;</span>
            </div>
            <div className="username-change">
              <span className="ui-preview-text" style={{width: random.int(30, 50) + "px"}}>&nbsp;</span>
              <span className="material-icon">
                arrow_forward
              </span>
              <span className="ui-preview-text" style={{width: random.int(30, 50) + "px"}}>&nbsp;</span>
            </div>
            <div className="username-change-date">
              <span className="ui-preview-text" style={{width: random.int(50, 100) + "px"}}>&nbsp;</span>
            </div>
          </li>
        })}
      </ul>
    </div>;
    /* jshint ignore:end */
  }

  render() {
    if (this.props.isLoaded) {
      if (this.props.changes.length) {
        return this.renderHistory();
      } else {
        return this.renderEmptyHistory();
      }
    } else {
      return this.renderHistoryPreview();
    }
  }
}

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoaded: false,
      options: null
    };
  }

  componentDidMount() {
    title.set({
      title: gettext("Change username"),
      parent: gettext("Change your options")
    });

    Promise.all([
      ajax.get(this.props.user.api_url.username),
      ajax.get(misago.get('USERNAME_CHANGES_API'), {user: this.props.user.id})
    ]).then((data) => {
      this.setState({
        isLoaded: true,
        options: {
          changes_left: data[0].changes_left,
          length_min: data[0].length_min,
          length_max: data[0].length_max,
          next_on: data[0].next_on ? moment(data[0].next_on) : null,
        }
      });

      store.dispatch(dehydrate(data[1].results));
    });
  }

  /* jshint ignore:start */
  onComplete = (username, slug, options) => {
    this.setState({
      options
    });

    store.dispatch(
      addNameChange({ username, slug }, this.props.user, this.props.user));
    store.dispatch(
      updateUsername(this.props.user, username, slug));

    snackbar.success(gettext("Your username has been changed successfully."));
  };
  /* jshint ignore:end */

  getChangeForm() {
    if (this.state.isLoaded) {
      if (this.state.options.changes_left > 0) {
        /* jshint ignore:start */
        return <ChangeUsername user={this.props.user}
                               options={this.state.options}
                               complete={this.onComplete} />;
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return <NoChangesLeft options={this.state.options} />;
        /* jshint ignore:end */
      }
    } else {
      /* jshint ignore:start */
      return <ChangeUsernameLoading />;
      /* jshint ignore:end */
    }
  }

  render() {
    /* jshint ignore:start */
    return <div>
      {this.getChangeForm()}
      <UsernameHistory isLoaded={this.state.isLoaded}
                       changes={this.props['username-history']} />
    </div>
    /* jshint ignore:end */
  }
}