import { Trans } from "@lingui/macro"
import React from "react"
import ThreadsModerationModal from "../ThreadsModerationModal"
import { ThreadsModerationModalAction } from "../ThreadsModerationModalContext"
import ThreadsModerationModalDeleteForm from "./ThreadsModerationModalDeleteForm"

const ThreadsModerationModalDelete: React.FC = () => (
  <ThreadsModerationModal
    action={ThreadsModerationModalAction.DELETE}
    title={<Trans id="moderation.delete_threads">Delete threads</Trans>}
  >
    {({ data: { category, threads }, close }) => {
      return (
        <ThreadsModerationModalDeleteForm
          category={category}
          threads={threads}
          close={close}
        />
      )
    }}
  </ThreadsModerationModal>
)

export default ThreadsModerationModalDelete
