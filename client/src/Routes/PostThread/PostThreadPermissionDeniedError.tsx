import { Trans } from "@lingui/macro"
import React from "react"
import { RoutePermissionDeniedError } from "../../UI/RouteError"

const PostThreadPermissionDeniedError: React.FC = () => (
  <RoutePermissionDeniedError
    header={
      <Trans id="post_thread.no_valid_categories_error">
        You don't have permission to post new threads.
      </Trans>
    }
    message={
      <Trans id="post_thread.no_valid_categories_error_message">
        No categories exist or you don't have permission to post thread in any
        of them.
      </Trans>
    }
  />
)

export default PostThreadPermissionDeniedError
