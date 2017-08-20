// jshint ignore:start
import React from 'react';
import DropdownMenu from '../dropdown-menu';
import { HEADER, RESULT, FOOTER } from './contants';
import flattenResults from './flatten-results';
import Footer from './footer';
import Header from './header';
import Result from './result';

export default function({ results, query }) {
  const flatResults = flattenResults(results);

  return (
    <DropdownMenu>
      {flatResults.map(({ provider, result, type }) => {
        if (type === HEADER) {
          return (
            <Header
              key={provider.id + type}
              provider={provider}
            />
          );
        } else if (type === FOOTER) {
          return (
            <Footer
              key={provider.id + type}
              provider={provider}
              query={query}
            />
          );
        } else {
          return (
            <Result
              key={provider.id + type + result.id}
              provider={provider}
              result={result}
            />
          );
        }
      })}
    </DropdownMenu>
  );
}