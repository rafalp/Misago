import React from 'react';
import { connect } from 'react-redux';
import { TabsNav, CompactNav } from 'misago/components/users/navs'; // jshint ignore:line
import ActivePosters from 'misago/components/users/active-posters/root'; // jshint ignore:line
import Rank from 'misago/components/users/rank/root';
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
    return <div className="page page-users-lists">

      <div className="page-header tabbed">
        <div className="container">

          <h1 className="pull-left">{gettext("Users")}</h1>

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
        <div className="page-tabs hidden-xs hidden-sm">
          <div className="container">

            <TabsNav lists={misago.get('USERS_LISTS')}
                     baseUrl={misago.get('USERS_LIST_URL')} />

          </div>
        </div>
      </div>
      <div className={this.getCompactNavClassName()}>

        <CompactNav lists={misago.get('USERS_LISTS')}
                    baseUrl={misago.get('USERS_LIST_URL')} />

      </div>

      {this.props.children}

    </div>;
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
        rank: {
          name: item.name,
          slug: item.slug,
          css_class: item.css_class,
          description: item.description
        }
      });
      paths.push({
        path: misago.get('USERS_LIST_URL') + item.slug + '/',
        component: connect(select)(Rank),
        rank: {
          name: item.name,
          slug: item.slug,
          css_class: item.css_class,
          description: item.description
        }
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
