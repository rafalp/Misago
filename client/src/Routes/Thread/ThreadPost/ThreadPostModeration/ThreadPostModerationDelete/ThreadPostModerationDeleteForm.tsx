import { Trans } from "@lingui/macro"
import React from "react"
import { Form, FormFooter } from "../../../../../UI/Form"
import {
  ModalAlert,
  ModalMessageBody,
  ModalFooter,
} from "../../../../../UI/Modal"
import RootError from "../../../../../UI/RootError"
import { IPost } from "../../../Thread.types"
import ThreadPostModerationError from "../ThreadPostModerationError"
import useDeleteThreadPostMutation from "./useDeleteThreadPostMutation"

interface IThreadPostModerationDeleteFormProps {
  threadId: string
  post: IPost
  page?: number
  close: () => void
}

interface IFormValues {}

const ThreadPostModerationDeleteForm: React.FC<IThreadPostModerationDeleteFormProps> = ({
  threadId,
  post,
  page,
  close,
}) => {
  const {
    data,
    loading,
    deletePost,
    error: graphqlError,
  } = useDeleteThreadPostMutation()

  if (data?.deleteThreadPost.errors) {
    return (
      <ThreadPostModerationError
        errors={data.deleteThreadPost.errors}
        close={close}
        forDelete
      />
    )
  }

  return (
    <Form<IFormValues>
      id="delete_post_form"
      disabled={loading}
      onSubmit={async () => {
        try {
          const result = await deletePost(threadId, post, page)

          if (!result.data?.deleteThreadPost.errors) {
            close()
          }
        } catch (error) {
          // do nothing when deleteThread throws
          return
        }
      }}
    >
      <RootError graphqlError={graphqlError}>
        {({ message }) => <ModalAlert>{message}</ModalAlert>}
      </RootError>
      <ModalMessageBody
        header={
          <Trans id="moderation.delete_post_prompt">
            Are you sure you want to delete this post?
          </Trans>
        }
        message={
          <Trans id="moderation.delete_message">
            This action is not reversible!
          </Trans>
        }
      />
      <ModalFooter>
        <FormFooter
          submitText={
            <Trans id="moderation.delete_post.submit">Delete post</Trans>
          }
          loading={loading}
          danger
          onCancel={close}
        />
      </ModalFooter>
    </Form>
  )
}

export default ThreadPostModerationDeleteForm
