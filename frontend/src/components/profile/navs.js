import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Li from 'misago/components/li'; //jshint ignore:line
import FollowButton from 'misago/components/profile/follow-button'; // jshint ignore:line
import misago from 'misago/index'; //jshint ignore:line

export class SideNav extends React.Component {
  render() {
    // jshint ignore:start
    return (
      <div className="list-group nav-side">
        {this.props.pages.map((page) => {
          return (
            <Link
              to={this.props.baseUrl + page.component + '/'}
              className="list-group-item"
              activeClassName="active"
              key={page.component}
            >
              <span className="material-icon">
                {page.icon}
              </span>
              {page.name}
            </Link>
          );
        })}
      </div>
    );
    // jshint ignore:end
  }
}

// jshint ignore:start
export function CompactNav(props) {
  return (
    <div className="page-tabs hidden-md hidden-lg">
      <div className="container">
        <ul className="nav nav-pills" role="menu">
          {props.pages.map((page) => {
            return (
              <Li
                path={props.baseUrl + page.component + '/'}
                key={page.component}
              >
                <Link
                  to={props.baseUrl + page.component + '/'}
                  onClick={props.hideNav}
                >
                  <span className="material-icon">
                    {page.icon}
                  </span>
                  {page.name}
                </Link>
              </Li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
// jshint ignore:end