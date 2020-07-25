import { Plural } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { useBulkActionLimit } from "../../../../Context"
import { Form, FormFooter, ModalBody, ModalFooter } from "../../../../UI"
import { IPost, IThread } from "../../Thread.types"
import useDeletePostsMutation from "../deleteThreadPosts"

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
    data,
    loading,
    deletePosts,
    error: graphqlError
  } = useDeletePostsMutation()

  const bulkActionLimit = useBulkActionLimit()
  const DeleteThreadsSchema = Yup.object().shape({
    threads: Yup.array()
      .min(1, "value_error.list.min_items")
      .max(bulkActionLimit, "value_error.list.max_items"),
  })

  return (
    <Form<IFormValues>
      id="delete_threads_form"
      disabled={loading}
      defaultValues={{ threads }}
      validationSchema={DeleteThreadsSchema}
      onSubmit={async ({ clearError, setError, data: { threads } }) => {
        clearError()
        clearThreadsErrors()

        try {
          const result = await deletePosts(thread, posts, page)
          const { errors } = result.data?.deleteThreadReplies || {}

          if (errors) {
            setThreadsErrors(threads, errors)
            errors?.forEach(({ location, type, message }) => {
              const field = location.join(".")
              setError(field, type, message)
            })
          } else {
            close()
          }
        } catch (error) {
          // do nothing when deleteThreads throws
          return
        }
      }}
    >
      <ModalBody>
        <p>Delete selected posts?.</p>
        {data && <pre>{JSON.stringify(data)}</pre>}
      </ModalBody>
      <ModalFooter>
        <FormFooter
          submitText={
            <Plural
              id="moderation.delete_[posts].submit"
              value={posts.length}
              one="Delete # post"
              other="Delete # posts"
            />
          }
          loading={loading}
          danger
          onCancel={close}
        />
      </ModalFooter>
    </Form>
  )
}

export default ThreadPostsModerationDelete
