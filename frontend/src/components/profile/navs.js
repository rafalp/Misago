import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Li from 'misago/components/li'; //jshint ignore:line
import misago from 'misago/index'; //jshint ignore:line

export class SideNav extends React.Component {
  getMeta(meta) {
    if (meta) {
      // jshint ignore:start
      return <span className="badge">{this.props.profile[meta.attr]}</span>;
      // jshint ignore:end
    } else {
      return null;
    }
  }

  render() {
    // jshint ignore:start
    return <div className="list-group nav-side">
      {this.props.pages.map((page) => {
        return <Link to={this.props.baseUrl + page.component + '/'}
                     className="list-group-item"
                     activeClassName="active"
                     key={page.component}>
          <span className="material-icon">
            {page.icon}
          </span>
          {page.name}
          {this.getMeta(page.meta)}
        </Link>;
      })}
    </div>;
    // jshint ignore:end
  }
}

export class CompactNav extends SideNav {
  render() {
    // jshint ignore:start
    return <ul className="dropdown-menu" role="menu">
      {this.props.pages.map((page) => {
        return <Li path={this.props.baseUrl + page.component + '/'}
                   key={page.component}>
          <Link to={this.props.baseUrl + page.component + '/'}
                onClick={this.props.hideNav}>
            <span className="material-icon">
              {page.icon}
            </span>
            {page.name}
            {this.getMeta(page.meta)}
          </Link>
        </Li>;
      })}
    </ul>;
    // jshint ignore:end
  }
}