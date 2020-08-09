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
import useDeleteThreadPostsMutation from "./useDeleteThreadPostsMutation"

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
  } = useSelectionErrors<IPost>("posts")

  const {
    data,
    loading,
    deletePosts,
    error: graphqlError,
  } = useDeleteThreadPostsMutation()

  const bulkActionLimit = useBulkActionLimit()
  const DeletePostsSchema = Yup.object().shape({
    posts: Yup.array()
      .min(1, "value_error.list.min_items")
      .max(bulkActionLimit, "value_error.list.max_items"),
  })
  console.log(selectionErrors)
  if (data?.deleteThreadPosts.errors) {
    return (
      <ThreadPostsModerationError
        posts={posts}
        selectionErrors={selectionErrors}
        errors={data.deleteThreadPosts.errors}
        close={close}
        forDelete
      />
    )
  }

  return (
    <Form<IFormValues>
      id="delete_posts_form"
      disabled={loading}
      defaultValues={{ posts }}
      validationSchema={DeletePostsSchema}
      onSubmit={async ({ data: { posts } }) => {
        try {
          const result = await deletePosts(thread, posts, page)
          if (result.data?.deleteThreadPosts.errors) {
            console.log(posts, result.data?.deleteThreadPosts.errors)
            setSelectionErrors(posts, result.data.deleteThreadPosts.errors)
          } else {
            close()
          }
        } catch (error) {
          // do nothing when deletePosts throws
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
