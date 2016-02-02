import React from 'react';
import { connect } from 'react-redux';
import { SideNav, CompactNav } from 'misago/components/options/navs'; // jshint ignore:line
import ChangeForumOptions from 'misago/components/options/forum-options';
import ChangeUsername from 'misago/components/options/change-username';
import ChangeSignInCredentials from 'misago/components/options/sign-in-credentials';
import misago from 'misago/index';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      dropdown: false
    };
  }

  /* jshint ignore:start */
  toggleNav = () => {
    if (this.state.dropdown) {
      this.setState({
        dropdown: false
      });
    } else {
      this.setState({
        dropdown: true
      });
    }
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

  render() {
    /* jshint ignore:start */
    return <div className="page page-options">
      <div className="page-header">
        <div className="container">

          <h1 className="pull-left">{gettext("Change your options")}</h1>

          <button className="btn btn-default btn-icon btn-dropdown-toggle hidden-md hidden-lg"
                  type="button"
                  onClick={this.toggleNav}
                  aria-haspopup="true"
                  aria-expanded={this.state.dropdown ? 'true' : 'false'}>
            <i className="material-icon">
              menu
            </i>
          </button>

        </div>
      </div>
      <div className={this.getCompactNavClassName()}>

        <CompactNav options={misago.get('USER_OPTIONS')}
                    baseUrl={misago.get('USERCP_URL')} />

      </div>
      <div className="container">

        <div className="row">
          <div className="col-md-3 hidden-xs hidden-sm">

            <SideNav options={misago.get('USER_OPTIONS')}
                     baseUrl={misago.get('USERCP_URL')} />

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
    'username-history': store['username-history']
  };
}

export function paths() {
  return [
    {
      path: misago.get('USERCP_URL') + 'forum-options/',
      component: connect(select)(ChangeForumOptions)
    },
    {
      path: misago.get('USERCP_URL') + 'change-username/',
      component: connect(select)(ChangeUsername)
    },
    {
      path: misago.get('USERCP_URL') + 'sign-in-credentials/',
      component: connect(select)(ChangeSignInCredentials)
    }
  ];
}
