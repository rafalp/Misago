// jshint ignore:start
import React from 'react';
import Message from './message';

const MSG_START = gettext("To start search enter search query in field above.");
const MSG_EMPTY = gettext("Search returned no results.");

export default function({ isLoading, results, query }) {
  if (!query.trim().length) {
    return (
      <Message message={MSG_START} />
    );
  }

  if (results.length) {
    return (
      <Message message={"show results"} />
    );
  } else if (isLoading) {
    return (
      <Message message={"show loader"} />
    );
  }

  return (
    <Message message={MSG_EMPTY} />
  );
}