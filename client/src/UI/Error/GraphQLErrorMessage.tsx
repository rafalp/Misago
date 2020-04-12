import { Trans } from "@lingui/macro"
import React from "react"

const GraphQLErrorMessage: React.FC = () => (
  <Trans id="api_error.message">
    Site server can't be reached. You may be offline or the site is unavailable
    at the moment.
  </Trans>
)

export default GraphQLErrorMessage
