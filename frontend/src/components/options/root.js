import React from 'react'; // jshint ignore:line
import { connect } from 'react-redux';
import DropdownToggle from 'misago/components/dropdown-toggle'; // jshint ignore:line
import { SideNav, CompactNav } from 'misago/components/options/navs'; // jshint ignore:line
import DeleteAccount from 'misago/components/options/delete-account';
import EditDetails from 'misago/components/options/edit-details';
import ChangeForumOptions from 'misago/components/options/forum-options';
import ChangeUsername from 'misago/components/options/change-username/root';
import ChangeSignInCredentials from 'misago/components/options/sign-in-credentials/root';
import WithDropdown from 'misago/components/with-dropdown';
import misago from 'misago/index';

export default class extends WithDropdown {
  render() {
    /* jshint ignore:start */
    return (
      <div className="page page-options">
        <div className="page-header-bg">
          <div className="page-header">
            <div className="container">

              <h1>{gettext("Change your options")}</h1>

            </div>
            <div className="page-tabs visible-xs-block visible-sm-block">
              <div className="container">
                <CompactNav
                  className="nav nav-pills"
                  baseUrl={misago.get('USERCP_URL')}
                  options={misago.get('USER_OPTIONS')}
                />
              </div>
            </div>
          </div>
        </div>
        <div className="container">

          <div className="row">
            <div className="col-md-3 hidden-xs hidden-sm">

              <SideNav
                baseUrl={misago.get('USERCP_URL')}
                options={misago.get('USER_OPTIONS')}
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
    'username-history': store['username-history']
  };
}

export function paths() {
  const paths = [
    {
      path: misago.get('USERCP_URL') + 'forum-options/',
      component: connect(select)(ChangeForumOptions)
    },
    {
      path: misago.get('USERCP_URL') + 'edit-details/',
      component: connect(select)(EditDetails)
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

  if (misago.get('ENABLE_DELETE_OWN_ACCOUNT')) {
    paths.push({
      path: misago.get('USERCP_URL') + 'delete-account/',
      component: connect(select)(DeleteAccount)
    });
  }

  return paths;
}
