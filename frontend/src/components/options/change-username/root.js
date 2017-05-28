import moment from 'moment';
import React from 'react';
import FormLoading from 'misago/components/options/change-username/form-loading'; // jshint ignore:line
import FormLocked from 'misago/components/options/change-username/form-locked'; // jshint ignore:line
import Form from 'misago/components/options/change-username/form'; // jshint ignore:line
import UsernameHistory from 'misago/components/username-history/root'; // jshint ignore:line
import misago from 'misago/index';
import { hydrate, addNameChange } from 'misago/reducers/username-history'; // jshint ignore:line
import { updateUsername } from 'misago/reducers/users'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import title from 'misago/services/page-title';
import snackbar from 'misago/services/snackbar'; // jshint ignore:line
import store from 'misago/services/store';

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
      ajax.get(this.props.user.api.username),
      ajax.get(misago.get('USERNAME_CHANGES_API'), {user: this.props.user.id})
    ]).then((data) => {
      store.dispatch(hydrate(data[1].results));

      this.setState({
        isLoaded: true,
        options: {
          changes_left: data[0].changes_left,
          length_min: data[0].length_min,
          length_max: data[0].length_max,
          next_on: data[0].next_on ? moment(data[0].next_on) : null,
        }
      });
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
    if (!this.state.isLoaded) {
      /* jshint ignore:start */
      return (
        <FormLoading />
      );
      /* jshint ignore:end */
    }

    if (this.state.options.changes_left === 0) {
      /* jshint ignore:start */
      return (
        <FormLocked options={this.state.options} />
      );
      /* jshint ignore:end */
    }

    /* jshint ignore:start */
    return (
      <Form
        complete={this.onComplete}
        options={this.state.options}
        user={this.props.user}
      />
    );
    /* jshint ignore:end */
  }

  render() {
    /* jshint ignore:start */
    return (
      <div>
        {this.getChangeForm()}
        <UsernameHistory
          changes={this.props['username-history']}
          isLoaded={this.state.isLoaded}
        />
      </div>
    );
    /* jshint ignore:end */
  }
}