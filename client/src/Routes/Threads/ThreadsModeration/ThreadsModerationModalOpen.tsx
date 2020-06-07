import { Trans } from "@lingui/macro"
import React from "react"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"
import ThreadsModerationModalError from "./ThreadsModerationModalError"

const ThreadsModerationModalOpen: React.FC = () => (
  <ThreadsModerationModal
    action={ThreadsModerationModalAction.OPEN}
    title={<Trans id="moderation.open_threads">Open threads</Trans>}
  >
    {({ data: { threads, graphqlError, errors }, close }) => (
      <ThreadsModerationModalError
        graphqlError={graphqlError}
        errors={errors}
        threads={threads}
        close={close}
      />
    )}
  </ThreadsModerationModal>
)

export default ThreadsModerationModalOpen
