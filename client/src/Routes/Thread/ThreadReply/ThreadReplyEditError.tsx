import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import { ErrorMessage, GraphQLErrorMessage } from "../../../UI/Error"
import GraphQLErrorRenderer from "../../../UI/GraphQLErrorRenderer"
import { PostingFormError } from "../../../UI/PostingForm"
import ThreadReplyDialog from "./ThreadReplyDialog"

interface IThreadReplyEditErrorProps {
  error?: ApolloError
}

const ThreadReplyEditError: React.FC<IThreadReplyEditErrorProps> = ({
  error,
}) => (
  <ThreadReplyDialog>
    <PostingFormError
      error={
        <Trans id="posting.error">
          This form could not be displayed due to an error.
        </Trans>
      }
      detail={
        error ? (
          <GraphQLErrorRenderer
            error={error}
            queryError={<ErrorMessage />}
            networkError={<GraphQLErrorMessage />}
          />
        ) : (
          <Trans id="posting.post_not_found">
            Post to edit doesn't exist or you don't have permission to see it.
          </Trans>
        )
      }
    />
  </ThreadReplyDialog>
)

export default ThreadReplyEditError
