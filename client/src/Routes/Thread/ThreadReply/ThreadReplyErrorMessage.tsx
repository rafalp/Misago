import { Trans } from "@lingui/macro"
import React from "react"
import { PostingFormError } from "../../../UI/PostingForm"
import ThreadReplyDialog from "./ThreadReplyDialog"

const ThreadReplyErrorMessage: React.FC = () => (
  <ThreadReplyDialog>
    <PostingFormError
      error={
        <Trans id="posting.error">
          This form could not be displayed due to an error.
        </Trans>
      }
      detail={
        <Trans id="posting.error_detail">
          Please check your internet connection and try again later if the
          problem persists.
        </Trans>
      }
    />
  </ThreadReplyDialog>
)

export default ThreadReplyErrorMessage
