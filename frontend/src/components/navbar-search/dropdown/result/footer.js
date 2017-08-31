// jshint ignore:start
import React from 'react';

export default function({ provider, query }) {
  const url = provider.url + '?q=' + encodeURI(query);
  const label = gettext('See all %(count)s results in "%(provider)s".');

  return (
    <li className="dropdown-search-footer">
      <a href={url}>
        {interpolate(label, {
          count: provider.count,
          provider: provider.name
        }, true)}
      </a>
    </li>
  );
}