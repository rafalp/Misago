// jshint ignore:start
import React from 'react';
import Thread from './thread';
import User from './user';

export default function({ provider, result }) {
  if (provider.id === 'threads') {
    return (
      <Thread result={result} />
    );
  }

  return (
    <User result={result} />
  );
}