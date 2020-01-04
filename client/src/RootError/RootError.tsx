import React from "react"
import { Icon } from "../UI"

const RootError: React.FC = () => (
  <div className="root-error">
    <div className="root-error-body">
      <div className="root-error-icon">
        <Icon icon="exclamation-triangle" solid />
      </div>
      <div className="root-error-message">
        <h1>The site can't be loaded due to an error.</h1>
        <p>
          You may be disconnected from the internet or there is a problem with the site that
          prohibits it from loading correctly.
        </p>
      </div>
    </div>
  </div>
)

export default RootError
