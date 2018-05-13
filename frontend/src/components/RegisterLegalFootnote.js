/* jshint ignore:start */
import React from 'react';
import misago from 'misago';

const RegisterLegalFootnote = () => {
  if (!misago.get('TERMS_OF_SERVICE_URL')) return null;

  return (
    <p className="legal-footnote">
      <span className="material-icon">
        info_outline
        </span>
      <a
        href={misago.get('TERMS_OF_SERVICE_URL')}
        target="_blank"
      >
        {gettext("By registering you agree to site's terms and conditions.")}
      </a>
    </p>
  );
}

export default RegisterLegalFootnote;