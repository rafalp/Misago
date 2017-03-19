import React from 'react'; // jshint ignore:line
import { connect } from 'react-redux';
import DropdownToggle from 'misago/components/dropdown-toggle'; // jshint ignore:line
import { TabsNav, CompactNav } from 'misago/components/users/navs'; // jshint ignore:line
import ActivePosters from 'misago/components/users/active-posters/root'; // jshint ignore:line
import Rank from 'misago/components/users/rank/root';
import WithDropdown from 'misago/components/with-dropdown';
import misago from 'misago/index';

export default class extends WithDropdown {
  render() {
    /* jshint ignore:start */
    return (
      <div className="page page-users-lists">
        <div className="page-header tabbed">
          <div className="container">
            <h1>{gettext("Users")}</h1>
          </div>
          <div className="page-tabs hidden-xs">
            <div className="container">

              <TabsNav
                lists={misago.get('USERS_LISTS')}
                baseUrl={misago.get('USERS_LIST_URL')}
              />

            </div>
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
                lists={misago.get('USERS_LISTS')}
                baseUrl={misago.get('USERS_LIST_URL')}
              />
            </div>
          </div>
        </div>

        {this.props.children}
      </div>
    );
    /* jshint ignore:end */
  }
}

export function select(store) {
  return {
    'tick': store.tick.tick,
    'user': store.auth.user,
    'users': store.users
  };
}

export function paths() {
  let paths = [];

  misago.get('USERS_LISTS').forEach(function(item) {
    if (item.component === 'rank') {
      paths.push({
        path: misago.get('USERS_LIST_URL') + item.slug + '/:page/',
        component: connect(select)(Rank),
        rank: item
      });
      paths.push({
        path: misago.get('USERS_LIST_URL') + item.slug + '/',
        component: connect(select)(Rank),
        rank: item
      });
    } else if (item.component === 'active-posters'){
      paths.push({
        path: misago.get('USERS_LIST_URL') + item.component + '/',
        component: connect(select)(ActivePosters),
        extra: {
          name: item.name
        }
      });
    }
  });

  return paths;
}
