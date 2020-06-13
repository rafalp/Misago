import { Trans } from "@lingui/macro"
import React from "react"
import ThreadModerationModal from "./ThreadModerationModal"
import { ThreadModerationModalAction } from "./ThreadModerationModalContext"
import ThreadModerationModalError from "./ThreadModerationModalError"

const ThreadModerationModalClose: React.FC = () => (
  <ThreadModerationModal
    action={ThreadModerationModalAction.CLOSE}
    title={<Trans id="moderation.close_thread">Close thread</Trans>}
  >
    {({ data: { graphqlError, errors }, close }) => (
      <ThreadModerationModalError
        graphqlError={graphqlError}
        errors={errors}
        close={close}
      />
    )}
  </ThreadModerationModal>
)

export default ThreadModerationModalClose
