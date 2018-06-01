/* jshint ignore:start */
import React from 'react';

const Header = ({ backendName }) => {
  const pageTitleTpl = gettext("Sign in with %(backend)s");
  const pageTitle = interpolate(pageTitleTpl, { backend: backendName }, true);

  return (
    <div className="page-header-bg">
      <div className="page-header">
        <div className="container">
          <h1>
            {pageTitle}
          </h1>
        </div>
      </div>
    </div>
  );
}

export default Header;