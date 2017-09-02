// jshint ignore:start
import React from 'react';

export default function({ provider, query }) {
  const url = provider.url + '?q=' + encodeURI(query);
  const label = ngettext(
    'See full "%(provider)s" results page with %(count)s result.',
    'See full "%(provider)s" results page with %(count)s results.',
    provider.count
  );

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