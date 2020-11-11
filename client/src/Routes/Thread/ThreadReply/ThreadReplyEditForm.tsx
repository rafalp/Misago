import { Trans } from "@lingui/macro"
import React from "react"
import {
  PostingFormBody,
  PostingFormCollapsible,
  PostingFormDialog,
  PostingFormHeader,
} from "../../../UI/PostingForm"
import { useThreadReplyContext } from "./ThreadReplyContext"
import ThreadReplyDialog from "./ThreadReplyDialog"

const Editor = React.lazy(() => import("../../../Editor"))

interface IThreadReplyEditFormProps {
  threadId?: string
}

const ThreadReplyEditForm: React.FC<IThreadReplyEditFormProps> = ({
  threadId,
}) => {
  const context = useThreadReplyContext()

  if (!context) return null

  return (
    <ThreadReplyDialog>
      <Editor />
    </ThreadReplyDialog>
  )
}

export default ThreadReplyEditForm
