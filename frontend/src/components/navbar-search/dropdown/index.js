// jshint ignore:start
import React from 'react';
import Loader from './loader';
import Message from './message';
import Results from './results';

const MSG_START = gettext("To start search enter search query.");
const MSG_EMPTY = gettext("Search returned no results.");

export default function({ isLoading, results, query }) {
  if (!query.trim().length) {
    return (
      <Message message={MSG_START} />
    );
  }

  if (results.length) {
    return (
      <Results
        results={results}
        query={query}
      />
    );
  } else if (isLoading) {
    return (
      <Loader />
    );
  }

  return (
    <Message message={MSG_EMPTY} />
  );
}