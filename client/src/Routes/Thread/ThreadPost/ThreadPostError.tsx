import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import { ErrorMessage, GraphQLErrorMessage } from "../../../UI/Error"
import GraphQLErrorRenderer from "../../../UI/GraphQLErrorRenderer"

interface IThreadPostErrorProps {
  error?: ApolloError
  notfound?: boolean
}

const ThreadPostError: React.FC<IThreadPostErrorProps> = ({
  error,
  notfound,
}) => (
  <div className="card-body post-error">
    <div className="post-error-body">
      <div className="post-error-icon" />
      <div className="post-error-message">
        <p className="lead">
          <Trans id="post.error_message">
            This action is not available at the moment.
          </Trans>
        </p>
        {error && (
          <p>
            <GraphQLErrorRenderer
              error={error}
              networkError={<GraphQLErrorMessage />}
              queryError={<ErrorMessage />}
            />
          </p>
        )}
        {notfound && (
          <p>
            <Trans id="value_error.post.not_exists">
              Post could not be found.
            </Trans>
          </p>
        )}
      </div>
    </div>
  </div>
)

export default ThreadPostError
