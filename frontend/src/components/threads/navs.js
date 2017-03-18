import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Li from 'misago/components/li'; //jshint ignore:line

// jshint ignore:start
const navLinks = function(baseUrl, active, lists, hideNav) {
    return lists.map(function(list) {
      return <Li isControlled={true}
                 isActive={list.path === active.path}
                 key={baseUrl + list.path}>
        <Link to={baseUrl + list.path} onClick={hideNav}>
          <span className="hidden-xs">{list.name}</span>
          <span className="hidden-sm hidden-md hidden-lg">{list.longName}</span>
        </Link>
      </Li>;
  });
};
// jshint ignore:end

export class TabsNav extends React.Component {
  render() {
    // jshint ignore:start
    return (
      <div className="page-tabs hidden-xs hidden-sm">
        <div className="container">
          <ul className="nav nav-pills">
            {navLinks(this.props.baseUrl, this.props.list, this.props.lists, this.props.hideNav)}
          </ul>
        </div>
      </div>
    );
    // jshint ignore:end
  }
}

// jshint ignore:start
export function CompactNav(props) {
  return (
    <div className="dropdown">
      <button
        aria-expanded="true"
        aria-haspopup="true"
        className="btn btn-default dropdown-toggle btn-block"
        data-toggle="dropdown"
        type="button"
      >
        <span className="material-icon">
          filter_list
        </span>
        {props.list.longName}
      </button>
      <ul className="dropdown-menu stick-to-bottom">
        {navLinks(props.baseUrl, props.list, props.lists, props.hideNav)}
      </ul>
    </div>
  );

}
// jshint ignore:end