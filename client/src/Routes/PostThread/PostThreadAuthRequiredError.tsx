import { Trans } from "@lingui/macro"
import React from "react"
import { RouteAuthRequiredError } from "../../UI/RouteError"

const PostThreadAuthRequiredError: React.FC = () => (
  <RouteAuthRequiredError
    header={
      <Trans id="post_thread.auth_error">
        You must be logged in to post a new thread.
      </Trans>
    }
  />
)

export default PostThreadAuthRequiredError
