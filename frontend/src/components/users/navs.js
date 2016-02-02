import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line
import Li from 'misago/components/li'; //jshint ignore:line
import misago from 'misago/index'; //jshint ignore:line

// jshint ignore:start
let listUrl = function(baseUrl, list) {
  let url = baseUrl;
  if (list.component === 'rank') {
    url += list.slug;
  } else {
    url += list.component;
  }
  return url + '/';
};

let navLinks = function(baseUrl, lists) {
    return lists.map(function(list) {
      let url = listUrl(baseUrl, list);
      return <Li path={url}
                 key={url}>
        <Link to={url}>
          {list.name}
        </Link>
      </Li>;
  });
};
// jshint ignore:end

export class TabsNav extends React.Component {
  render() {
    // jshint ignore:start
    return <ul className="nav nav-pills">
      {navLinks(this.props.baseUrl, this.props.lists)}
    </ul>;
    // jshint ignore:end
  }
}

export class CompactNav extends React.Component {
  render() {
    // jshint ignore:start
    return <ul className="dropdown-menu" role="menu">
      {navLinks(this.props.baseUrl, this.props.lists)}
    </ul>;
    // jshint ignore:end
  }
}