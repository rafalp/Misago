import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Li from 'misago/components/li'; //jshint ignore:line
import misago from 'misago/index'; //jshint ignore:line

export class SideNav extends React.Component {
  render() {
    // jshint ignore:start
    return <div className="list-group nav-side">
      {this.props.options.map((option) => {
        return <Link to={this.props.baseUrl + option.component + '/'}
                     className="list-group-item"
                     activeClassName="active"
                     key={option.component}>
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
      {this.props.options.map((option) => {
        return <Li path={this.props.baseUrl + option.component + '/'}
                   key={option.component}>
          <Link to={this.props.baseUrl + option.component + '/'}
                onClick={this.props.hideNav}>
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