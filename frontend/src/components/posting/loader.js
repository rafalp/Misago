// jshint ignore:start
import React from 'react';
import Container from './container';
import Loader from 'misago/components/loader';

export default function(props) {
  return (
    <Container className="posting-loader">
      <Loader />
    </Container>
  );
}