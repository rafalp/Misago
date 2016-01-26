import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Li from 'misago/components/li'; //jshint ignore:line
import misago from 'misago/index'; //jshint ignore:line

export class SideNav extends React.Component {
  render() {
    // jshint ignore:start
    return <div className="list-group nav-side">
      {misago.get('USER_OPTIONS').map(function(option, i) {
        return <Link to={misago.get('USERCP_URL') + option.component + '/'}
                     className="list-group-item"
                     activeClassName="active"
                     key={i}>
          <span className="material-icon">
            {option.icon}
          </span>
          {option.name}
        </Link>;
      })}
    </div>;
    // jshint ignore:end
  }
}

export class CompactNav extends React.Component {
  render() {
    // jshint ignore:start
    return <ul className="dropdown-menu" role="menu">
      {misago.get('USER_OPTIONS').map(function(option, i) {
        return <Li path={misago.get('USERCP_URL') + option.component + '/'}
                   key={i}>
          <Link to={misago.get('USERCP_URL') + option.component + '/'}>
            <span className="material-icon">
              {option.icon}
            </span>
            {option.name}
          </Link>
        </Li>;
      })}
    </ul>;
    // jshint ignore:end
  }
}