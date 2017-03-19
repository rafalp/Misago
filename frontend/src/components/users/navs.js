// jshint ignore:start
import React from 'react';
import { Link } from 'react-router';
import Li from 'misago/components/li';
import misago from 'misago/index';

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
      return (
        <Li path={url} key={url}>
          <Link to={url}>
            {list.name}
          </Link>
        </Li>
      );
  });
};

export function TabsNav(props) {
  return (
    <ul className="nav nav-pills">
      {navLinks(props.baseUrl, props.lists)}
    </ul>
  );
}

export function CompactNav(props){
  return (
    <ul className={props.className || "dropdown-menu stick-to-bottom"} role="menu">
      {navLinks(props.baseUrl, props.lists)}
    </ul>
  );
}