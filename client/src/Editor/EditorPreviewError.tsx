import { Trans } from "@lingui/macro"
import { ApolloError } from "apollo-client"
import React from "react"
import { ErrorMessage, GraphQLErrorMessage } from "../UI/Error"
import GraphQLErrorRenderer from "../UI/GraphQLErrorRenderer"

interface EditorPreviewErrorProps {
  error: ApolloError
}

const EditorPreviewError: React.FC<EditorPreviewErrorProps> = ({ error }) => (
  <div className="form-editor-preview form-editor-preview-error">
    <div className="form-editor-preview-error-body">
      <div className="form-editor-preview-error-icon" />
      <div className="form-editor-preview-error-message">
        <p className="lead">
          <Trans id="editor.error_message">Preview could not be loaded.</Trans>
        </p>
        <p>
          <GraphQLErrorRenderer
            error={error}
            networkError={<GraphQLErrorMessage />}
            queryError={<ErrorMessage />}
          />
        </p>
      </div>
    </div>
  </div>
)

export default EditorPreviewError
