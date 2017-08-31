// jshint ignore:start
import React from 'react';
import { HEADER, FOOTER } from '../constants';
import Footer from './footer';
import Header from './header';
import Result from './result';

export default function({ provider, result, type, query }) {
  if (type === HEADER) {
    return (
      <Header provider={provider} />
    );
  } else if (type === FOOTER) {
    return (
      <Footer provider={provider} query={query} />
    );
  }

  return (
    <Result provider={provider} result={result} />
  );
}