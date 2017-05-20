import moment from 'moment';
import React from 'react';
import PanelLoader from 'misago/components/panel-loader'; // jshint ignore:line
import PanelMessage from 'misago/components/panel-message'; // jshint ignore:line
import misago from 'misago/index';
import polls from 'misago/services/polls';
import title from 'misago/services/page-title';

export default class extends React.Component {
  constructor(props) {
    super(props);

    if (misago.has('PROFILE_BAN')) {
      this.initWithPreloadedData(misago.pop('PROFILE_BAN'));
    } else {
      this.initWithoutPreloadedData();
    }

    this.startPolling(props.profile.api.ban);
  }

  initWithPreloadedData(ban) {
    if (ban.expires_on) {
      ban.expires_on = moment(ban.expires_on);
    }

    this.state = {
      isLoaded: true,
      ban
    };
  }

  initWithoutPreloadedData() {
    this.state = {
      isLoaded: false
    };
  }

  startPolling(api) {
    polls.start({
      poll: 'ban-details',
      url: api,
      frequency: 90 * 1000,
      update: this.update,
      error: this.error
    });
  }

  /* jshint ignore:start */
  update = (ban) => {
    if (ban.expires_on) {
      ban.expires_on = moment(ban.expires_on);
    }

    this.setState({
      isLoaded: true,
      error: null,

      ban
    });
  };

  error = (error) => {
    this.setState({
      isLoaded: true,
      error: error.detail,
      ban: null
    });
  };
  /* jshint ignore:end */

  componentDidMount() {
    title.set({
      title: gettext("Ban details"),
      parent: this.props.profile.username
    });
  }

  componentWillUnmount() {
    polls.stop('ban-details');
  }

  getUserMessage() {
    if (this.state.ban.user_message) {
      /* jshint ignore:start */
      return <div className="panel-body ban-message ban-user-message">
        <h4>{gettext("User-shown ban message")}</h4>
        <div className="lead" dangerouslySetInnerHTML={{
            __html: this.state.ban.user_message.html
          }} />
      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getStaffMessage() {
    if (this.state.ban.staff_message) {
      /* jshint ignore:start */
      return <div className="panel-body ban-message ban-staff-message">
        <h4>{gettext("Team-shown ban message")}</h4>
        <div className="lead" dangerouslySetInnerHTML={{
            __html: this.state.ban.staff_message.html
          }} />
      </div>;
      /* jshint ignore:end */
      } else {
      return null;
    }
  }

  getExpirationMessage() {
    if (this.state.ban.expires_on) {
      if (this.state.ban.expires_on.isAfter(moment())) {
        /* jshint ignore:start */
        let title = interpolate(
          gettext("This ban expires on %(expires_on)s."), {
            'expires_on': this.state.ban.expires_on.format('LL, LT')
          }, true);

        let message = interpolate(
          gettext("This ban expires %(expires_on)s."), {
            'expires_on': this.state.ban.expires_on.fromNow()
          }, true);

        return <abbr title={title}>
          {message}
        </abbr>;
        /* jshint ignore:end */
      } else {
        return gettext("This ban has expired.");
      }
    } else {
      return interpolate(gettext("%(username)s's ban is permanent."), {
        'username': this.props.profile.username
      }, true);
    }
  }

  getPanelBody() {
    if (this.state.ban) {
      if (Object.keys(this.state.ban).length) {
        /* jshint ignore:start */
        return <div>
          {this.getUserMessage()}
          {this.getStaffMessage()}

          <div className="panel-body ban-expires">
            <h4>{gettext("Ban expiration")}</h4>
            <p className="lead">
              {this.getExpirationMessage()}
            </p>
          </div>
        </div>;
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return <div>
          <PanelMessage message={gettext("No ban is active at the moment.")} />
        </div>;
        /* jshint ignore:end */
      }
    } else if (this.state.error) {
      /* jshint ignore:start */
      return <div>
        <PanelMessage icon="error_outline"
                      message={this.state.error} />
      </div>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <div>
        <PanelLoader />
      </div>;
      /* jshint ignore:end */
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="profile-ban-details">
      <div className="panel panel-default">
        <div className="panel-heading">
          <h3 className="panel-title">{gettext("Ban details")}</h3>
        </div>

        {this.getPanelBody()}

      </div>
    </div>;
    /* jshint ignore:end */
  }
}