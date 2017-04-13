// jshint ignore:start
import React from 'react';
import { Link } from 'react-router';
import Li from 'misago/components/li';
import misago from 'misago/index';

export default function({ baseUrl, lists }) {
  return (
    <ul className="nav nav-pills">
      {lists.map((list) => {
        const url = listUrl(baseUrl, list);
        return (
          <Li path={url} key={url}>
            <Link to={url}>
              {list.name}
            </Link>
          </Li>
        );
      })}
    </ul>
  );
}

const listUrl = function(baseUrl, list) {
  let url = baseUrl;
  if (list.component === 'rank') {
    url += list.slug;
  } else {
    url += list.component;
  }
  return url + '/';
};