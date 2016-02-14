import React from 'react';
import { connect } from 'react-redux';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import Header from 'misago/components/profile/Header'; // jshint ignore:line
import ModerationNav from 'misago/components/profile/moderation/nav'; // jshint ignore:line
import { SideNav, CompactNav } from 'misago/components/profile/navs'; // jshint ignore:line
import misago from 'misago/index';
import { dehydrate } from 'misago/reducers/profile'; // jshint ignore:line
import polls from 'misago/services/polls';
import store from 'misago/services/store'; // jshint ignore:line

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      dropdown: false
    };

    this.startPolling(props.profile.api_url.root);
  }

  startPolling(api) {
    polls.start({
      poll: 'user-profile',
      url: api,
      frequency: 90 * 1000,
      update: this.update
    });
  }

  /* jshint ignore:start */
  update = (data) => {
    store.dispatch(dehydrate(data));
  };
  /* jshint ignore:end */

  /* jshint ignore:start */
  toggleNav = () => {
    if (this.state.dropdown === 'pages') {
      this.setState({
        dropdown: false
      });
    } else {
      this.setState({
        dropdown: 'pages'
      });
    }
  };

  toggleModeration = () => {
    if (this.state.dropdown === 'moderation') {
      this.setState({
        dropdown: false
      });
    } else {
      this.setState({
        dropdown: 'moderation'
      });
    }
  };

  hideNav = () => {
    this.setState({
      dropdown: false
    });
  };
  /* jshint ignore:end */

  getToggleNavClassName() {
    if (this.state.dropdown) {
      return 'btn btn-default btn-icon open';
    } else {
      return 'btn btn-default btn-icon';
    }
  }

  getCompactNavClassName() {
    if (this.state.dropdown) {
      return 'compact-nav open';
    } else {
      return 'compact-nav';
    }
  }

  getNavDropdown() {
    if (this.state.dropdown === 'pages') {
      /* jshint ignore:start */
      return <CompactNav pages={misago.get('PROFILE_PAGES')}
                         baseUrl={misago.get('PROFILE').absolute_url}
                         profile={this.props.profile}
                         toggleModeration={this.toggleModeration}
                         hideNav={this.hideNav} />;
      /* jshint ignore:end */
    } else if (this.state.dropdown === 'moderation') {
      /* jshint ignore:start */
      return <ModerationNav profile={this.props.profile}
                            toggleNav={this.toggleNav}
                            hideNav={this.hideNav} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getClassName() {
    const baseClass = 'page page-user-profile';
    if (false && this.props.profile.rank.css_class) {
      return baseClass + ' page-user-profile-' + this.props.profile.rank.css_class;
    } else {
      return baseClass;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>

      <Header user={this.props.user}
              profile={this.props.profile}
              toggleNav={this.toggleNav}
              toggleModeration={this.toggleModeration} />

      <div className={this.getCompactNavClassName()}>
        {this.getNavDropdown()}
      </div>
      <div className="container">

        <div className="row">
          <div className="col-md-3 hidden-xs hidden-sm">

            <div className="profile-side-avatar">
              <Avatar user={this.props.profile} size="400" />
            </div>

            <SideNav pages={misago.get('PROFILE_PAGES')}
                     baseUrl={misago.get('PROFILE').absolute_url}
                     profile={this.props.profile} />

          </div>
          <div className="col-md-9">

            {this.props.children}

          </div>
        </div>

      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export function select(store) {
  return {
    'tick': store.tick.tick,
    'user': store.auth.user,
    'users': store.users,
    'profile': store.profile,
    'username-history': store['username-history']
  };
}

class Placeholder extends React.Component {
  render() {
    // jshint ignore:start
    return <div className="container">
      <p>{"Hello, I'm placeholder for " + this.props.route.name}</p>
    </div>;
    // jshint ignore:end
  }
}

const COMPONENTS = {
  'posts': Placeholder,
  'threads': Placeholder,
  'followers': Placeholder,
  'follows': Placeholder,
  'username-history': Placeholder,
  'ban-details': Placeholder
};

export function paths() {
  let paths = [];

  misago.get('PROFILE_PAGES').forEach(function(item) {
    paths.push(Object.assign({}, item, {
      path: misago.get('PROFILE').absolute_url + item.component + '/',
      component: connect(select)(COMPONENTS[item.component]),
    }));
  });

  return paths;
}
