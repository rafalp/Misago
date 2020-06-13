import React from "react"

const AppError: React.FC = () => (
  <div className="app-error">
    <div className="app-error-body">
      <div className="app-error-icon" />
      <div className="app-error-message">
        <h1>The site can't be loaded due to an error.</h1>
        <p>
          You may be disconnected from the internet or there is a problem with
          the site that prevents it from loading correctly.
        </p>
      </div>
    </div>
  </div>
)

export default AppError
