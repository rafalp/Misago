import { Trans } from "@lingui/macro"
import React from "react"
import ThreadModerationModal from "./ThreadModerationModal"
import { ThreadModerationModalAction } from "./ThreadModerationModalContext"
import ThreadModerationModalError from "./ThreadModerationModalError"

const ThreadModerationModalOpen: React.FC = () => (
  <ThreadModerationModal
    action={ThreadModerationModalAction.OPEN}
    title={<Trans id="moderation.open_thread">Open thread</Trans>}
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

export default ThreadModerationModalOpen
