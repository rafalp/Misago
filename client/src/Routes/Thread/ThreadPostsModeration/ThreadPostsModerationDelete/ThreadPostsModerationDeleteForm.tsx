import { Trans } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { useBulkActionLimit } from "../../../../Context"
import {
  Form,
  FormFooter,
  ModalAlert,
  ModalFormBody,
  ModalFooter,
  RootError,
  useSelectionErrors,
} from "../../../../UI"
import { IPost, IThread } from "../../Thread.types"
import ThreadPostsModerationError from "../ThreadPostsModerationError"
import ThreadPostsModerationSelectedPosts from "../ThreadPostsModerationSelectedPosts"
import useDeleteRepliesMutation from "../deleteThreadReplies"

interface IThreadPostsModerationDeleteProps {
  thread: IThread
  posts: Array<IPost>
  page: number | undefined
  close: () => void
}

interface IFormValues {
  posts: Array<IPost>
}

const ThreadPostsModerationDelete: React.FC<IThreadPostsModerationDeleteProps> = ({
  thread,
  posts,
  page,
  close,
}) => {
  const {
    errors: selectionErrors,
    setErrors: setSelectionErrors,
  } = useSelectionErrors<IPost>("replies")

  const {
    data,
    loading,
    deleteReplies,
    error: graphqlError,
  } = useDeleteRepliesMutation()

  const bulkActionLimit = useBulkActionLimit()
  const DeleteRepliesSchema = Yup.object().shape({
    posts: Yup.array()
      .min(1, "value_error.list.min_items")
      .max(bulkActionLimit, "value_error.list.max_items"),
  })
  console.log(selectionErrors)
  if (data?.deleteThreadReplies.errors) {
    return (
      <ThreadPostsModerationError
        posts={posts}
        selectionErrors={selectionErrors}
        errors={data.deleteThreadReplies.errors}
        forDelete
      />
    )
  }

  return (
    <Form<IFormValues>
      id="delete_replies_form"
      disabled={loading}
      defaultValues={{ posts }}
      validationSchema={DeleteRepliesSchema}
      onSubmit={async ({ data: { posts } }) => {
        try {
          const result = await deleteReplies(thread, posts, page)
          if (result.data?.deleteThreadReplies.errors) {
            console.log(posts, result.data?.deleteThreadReplies.errors)
            setSelectionErrors(posts, result.data.deleteThreadReplies.errors)
          } else {
            close()
          }
        } catch (error) {
          // do nothing when deleteReplies throws
          return
        }
      }}
    >
      <RootError graphqlError={graphqlError}>
        {({ message }) => <ModalAlert>{message}</ModalAlert>}
      </RootError>
      <ModalFormBody>
        <ThreadPostsModerationSelectedPosts
          max={bulkActionLimit}
          min={1}
          posts={posts}
        />
      </ModalFormBody>
      <ModalFooter>
        <FormFooter
          submitText={<Trans id="moderation.delete">Delete</Trans>}
          loading={loading}
          danger
          onCancel={close}
        />
      </ModalFooter>
    </Form>
  )
}

export default ThreadPostsModerationDelete
