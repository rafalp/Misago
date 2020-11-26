import { Trans } from "@lingui/macro"
import React from "react"
import { useModalContext } from "../../../../../Context"
import { Modal, ModalDialog } from "../../../../../UI/Modal"
import { IPost } from "../../../Thread.types"
import ThreadPostModerationDeleteForm from "./ThreadPostModerationDeleteForm"

interface IThreadPostModerationDeleteProps {
  threadId: string
  post: IPost
  page?: number
}

const ThreadPostModerationDelete: React.FC<IThreadPostModerationDeleteProps> = ({
  threadId,
  post,
  page,
}) => {
  const { isOpen, closeModal } = useModalContext()

  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={<Trans id="moderation.delete_post">Delete post</Trans>}
        close={closeModal}
      >
        <ThreadPostModerationDeleteForm
          threadId={threadId}
          post={post}
          page={page}
          close={closeModal}
        />
      </ModalDialog>
    </Modal>
  )
}
export default ThreadPostModerationDelete
