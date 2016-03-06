import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Li from 'misago/components/li'; //jshint ignore:line

// jshint ignore:start
let navLinks = function(baseUrl, active, lists, hideNav) {
    return lists.map(function(list) {
      return <Li isControlled={true}
                 isActive={list.path === active.path}
                 key={baseUrl + list.path}>
        <Link to={baseUrl + list.path} onClick={hideNav}>
          <span className="hidden-xs hidden-sm">{list.name}</span>
          <span className="hidden-md hidden-lg">{list.longName}</span>
        </Link>
      </Li>;
  });
};
// jshint ignore:end

export class TabsNav extends React.Component {
  render() {
    // jshint ignore:start
    return <div className="page-tabs hidden-xs hidden-sm">
      <div className="container">
        <ul className="nav nav-pills">
          {navLinks(this.props.baseUrl, this.props.list, this.props.lists, this.props.hideNav)}
        </ul>
      </div>
    </div>;
    // jshint ignore:end
  }
}

export class CompactNav extends React.Component {
  render() {
    // jshint ignore:start
    return <ul className="dropdown-menu" role="menu">
      {navLinks(this.props.baseUrl, this.props.list, this.props.lists, this.props.hideNav)}
    </ul>;
    // jshint ignore:end
  }
}