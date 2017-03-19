import React from 'react'; // jshint ignore:line
import { connect } from 'react-redux';
import BanDetails from './ban-details'; // jshint ignore:line
import { Posts, Threads } from './feed'; // jshint ignore:line
import Followers from './followers'; // jshint ignore:line
import Follows from './follows'; // jshint ignore:line
import UsernameHistory from './username-history'; // jshint ignore:line
import Header from './header'; // jshint ignore:line
import ModerationNav from './moderation/nav'; // jshint ignore:line
import { SideNav, CompactNav } from './navs'; // jshint ignore:line
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import WithDropdown from 'misago/components/with-dropdown';
import misago from 'misago';
import { hydrate } from 'misago/reducers/profile'; // jshint ignore:line
import polls from 'misago/services/polls';
import store from 'misago/services/store'; // jshint ignore:line

export default class extends WithDropdown {
  constructor(props) {
    super(props);

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
    store.dispatch(hydrate(data));
  };

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
  /* jshint ignore:end */

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
    const pages = misago.get('PROFILE_PAGES');

    return (
      <div className={this.getClassName()}>

        <Header
          user={this.props.user}
          profile={this.props.profile}
          toggleNav={this.toggleNav}
          toggleModeration={this.toggleModeration}
        />

        <div className="page-header page-header-followup visible-sm-block">
          <div className="container">
            <CompactNav
              className="nav nav-pills"
              pages={pages}
              baseUrl={misago.get('PROFILE').absolute_url}
              profile={this.props.profile}
            />
          </div>
        </div>

        <div className="page-header page-header-followup visible-xs-block">
          <div className="container">
            <div className="dropdown">
              <button
                aria-expanded="true"
                aria-haspopup="true"
                className="btn btn-default dropdown-toggle btn-block"
                data-toggle="dropdown"
                type="button"
              >
                <span className="material-icon">
                  menu
                </span>
                {gettext("Menu")}
              </button>
              <CompactNav
                pages={pages}
                baseUrl={misago.get('PROFILE').absolute_url}
                profile={this.props.profile}
              />
            </div>
          </div>
        </div>
        <div className="container">

          <div className="row">
            <div className="col-md-3 hidden-xs hidden-sm">

              <div className="profile-side-avatar">
                <Avatar user={this.props.profile} size="400" />
              </div>

              <SideNav
                pages={pages}
                baseUrl={misago.get('PROFILE').absolute_url}
                profile={this.props.profile}
              />

            </div>
            <div className="col-md-9">
              {this.props.children}
            </div>
          </div>

        </div>
      </div>
    );
    /* jshint ignore:end */
  }
}

export function select(store) {
  return {
    'tick': store.tick.tick,
    'user': store.auth.user,
    'users': store.users,
    'posts': store.posts,
    'profile': store.profile,
    'username-history': store['username-history']
  };
}

const COMPONENTS = {
  'posts': Posts,
  'threads': Threads,
  'followers': Followers,
  'follows': Follows,
  'username-history': UsernameHistory,
  'ban-details': BanDetails
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
