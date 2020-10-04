import { Trans } from "@lingui/macro"
import React from "react"
import { FormContext as HookFormContext } from "react-hook-form"
import { Redirect } from "react-router-dom"
import Editor from "../../../Editor"
import { useToastsContext } from "../../../Context"
import { FormContext } from "../../../UI/Form"
import * as urls from "../../../urls"
import { useThreadReplyContext } from "./ThreadReplyContext"
import usePostReplyMutation from "./usePostReplyMutation"

interface IThreadReplyFormProps {
  threadId: string
}

const ThreadReplyForm: React.FC<IThreadReplyFormProps> = ({ threadId }) => {
  const { showToast } = useToastsContext()
  const context = useThreadReplyContext()
  const [
    postReply,
    { data, loading, error: graphqlError },
  ] = usePostReplyMutation()

  if (data?.postReply.thread && data?.postReply.post) {
    return (
      <Redirect
        to={urls.threadPost(data.postReply.thread, data.postReply.post)}
      />
    )
  }

  if (!context) return null
  const { form } = context

  return (
    <HookFormContext {...form}>
      <FormContext.Provider
        value={{ disabled: loading, id: "thread_post_reply" }}
      >
        <form
          onSubmit={form.handleSubmit(async (data, event) => {
            if (loading) {
              event?.preventDefault()
              return
            }

            form.clearError()

            const result = await postReply({
              variables: {
                input: {
                  thread: threadId,
                  markup: data.markup,
                },
              },
            })
            const { errors, post } = result.data?.postReply || {}

            errors?.forEach(({ location, type, message }) => {
              const field = location.join(".") as "markup"
              form.setError(field, type, message)
            })

            if (post) {
              showToast(
                <Trans id="post_reply.message">Reply has been posted.</Trans>
              )
            }
          })}
        >
          <Editor name="markup" disabled={loading} />
          <button type="submit">Post reply</button>
        </form>
      </FormContext.Provider>
    </HookFormContext>
  )
}

export default ThreadReplyForm
