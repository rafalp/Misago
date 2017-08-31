// jshint ignore:start
import React from 'react';
import { RESULT } from './constants';
import DropdownMenu from './dropdown-menu';
import Loader from './loader';
import Message from './message';
import Result from './result';
import flattenResults from './flatten-results';

const MSG_START = gettext("To start search enter search query.");
const MSG_EMPTY = gettext("Search returned no results.");

export default function({ isLoading, onChange, results, query }) {
  if (!query.trim().length) {
    return (
      <DropdownMenu onChange={onChange} query={query}>
        <Message message={MSG_START} />
      </DropdownMenu>
    );
  }

  if (results.length) {
    const flatResults = flattenResults(results);

    return (
      <DropdownMenu onChange={onChange} query={query}>
        {flatResults.map((props) => {
          const { type, provider, result } = props;

          if (type === RESULT) {
            return (
              <Result
                key={[provider.id, type, result.id].join('_')}
                {...props}
              />
            );
          }

          return (
            <Result
              key={[provider.id, type].join('_')}
              query={query}
              {...props}
            />
          );
        })}
      </DropdownMenu>
    );
  } else if (isLoading) {
    return (
      <DropdownMenu onChange={onChange} query={query}>
        <Loader />
      </DropdownMenu>
    );
  }

  return (
    <DropdownMenu onChange={onChange} query={query}>
      <Message message={MSG_EMPTY} />
    </DropdownMenu>
  );
}