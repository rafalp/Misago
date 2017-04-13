import React from 'react'; // jshint ignore:line
import { connect } from 'react-redux';
import DropdownToggle from 'misago/components/dropdown-toggle'; // jshint ignore:line
import Nav from 'misago/components/users/nav'; // jshint ignore:line
import ActivePosters from 'misago/components/users/active-posters/root'; // jshint ignore:line
import Rank from 'misago/components/users/rank/root';
import WithDropdown from 'misago/components/with-dropdown';
import misago from 'misago/index';

export default class extends WithDropdown {
  render() {
    /* jshint ignore:start */
    return (
      <div className="page page-users-lists">
        <div className="page-header-bg">
          <div className="page-header">
            <div className="container">
              <h1>{gettext("Users")}</h1>
            </div>
            <div className="page-tabs">
              <div className="container">

                <Nav
                  lists={misago.get('USERS_LISTS')}
                  baseUrl={misago.get('USERS_LIST_URL')}
                />

              </div>
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
