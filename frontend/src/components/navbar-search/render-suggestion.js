// jshint ignore:start
import React from 'react';

export default function(suggestion) {
  const { section } = suggestion;

  if (section.id === 'threads') {
    return renderThread(suggestion);
  }

  if (section.id === 'users') {
    return renderUser(suggestion);
  }
  console.log(suggestion)
  return null;
};

export function renderThread(suggestion) {
  return (
    <div>
      {suggestion.thread.title}
    </div>
  );
}

export function renderUser(suggestion) {
  return (
    <div>
      {suggestion.username}
    </div>
  );
}