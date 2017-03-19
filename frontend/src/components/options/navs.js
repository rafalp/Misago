// jshint ignore:start
import React from 'react';
import { Link } from 'react-router';
import Li from 'misago/components/li';
import misago from 'misago/index';

export function SideNav(props) {
  return (
    <div className="list-group nav-side">
      {props.options.map((option) => {
        return (
          <Link
            to={props.baseUrl + option.component + '/'}
            className="list-group-item"
            activeClassName="active"
            key={option.component}
          >
            <span className="material-icon">
              {option.icon}
            </span>
            {option.name}
          </Link>
        );
      })}
    </div>
  );
}

export function CompactNav(props) {
  return (
    <ul className={props.className || "dropdown-menu stick-to-bottom"} role="menu">
      {props.options.map((option) => {
        return (
          <Li
            path={props.baseUrl + option.component + '/'}
            key={option.component}
          >
            <Link
              to={props.baseUrl + option.component + '/'}
              onClick={props.hideNav}
            >
              <span className="material-icon hidden-sm">
                {option.icon}
              </span>
              {option.name}
            </Link>
          </Li>
        );
      })}
    </ul>
  );
}