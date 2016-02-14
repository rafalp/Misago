import React from 'react';
import Button from 'misago/components/button'; // jshint ignore:line
import { patchProfile } from 'misago/reducers/profile'; // jshint ignore:line
import ajax from 'misago/services/ajax'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line
import store from 'misago/services/store'; // jshint ignore:line

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false
    };
  }

  getClassName() {
    if (this.props.profile.is_followed) {
      return this.props.className + ' btn-default btn-following';
    } else {
      return this.props.className + ' btn-default btn-follow';
    }
  }

  getIcon() {
    if (this.props.profile.is_followed) {
      return 'favorite';
    } else {
      return 'favorite_border';
    }
  }

  getLabel() {
    if (this.props.profile.is_followed) {
      return gettext('Following');
    } else {
      return gettext('Follow');
    }
  }

  /* jshint ignore:start */
  action = () => {
    this.setState({
      isLoading: true
    });

    if (this.props.profile.is_followed) {
      store.dispatch(patchProfile({
        is_followed: false,
        followers: this.props.profile.followers - 1
      }));
    } else {
      store.dispatch(patchProfile({
        is_followed: true,
        followers: this.props.profile.followers + 1
      }));
    }

    ajax.post(this.props.profile.api_url.follow).then((data) => {
      this.setState({
        isLoading: false
      });

      store.dispatch(patchProfile(data));
    }, function(rejection) {
      snackbar.apiError(rejection);
      this.setState({
        isLoading: false
      });
    });
  };
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    return <Button className={this.getClassName()}
                   disabled={this.state.isLoading}
                   onClick={this.action}>
      <span className="material-icon">
        {this.getIcon()}
      </span>
      {this.getLabel()}
    </Button>;
    /* jshint ignore:end */
  }
}