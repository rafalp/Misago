import { Trans } from "@lingui/macro"
import React from "react"
import { FormContext as HookFormContext } from "react-hook-form"
import { Redirect } from "react-router-dom"
import { useSettingsContext, useToastsContext } from "../../../Context"
import { ButtonPrimary } from "../../../UI/Button"
import { Field, FieldErrorFloating, FormContext } from "../../../UI/Form"
import { PostingFormAlert, PostingFormLoader } from "../../../UI/PostingForm"
import { ValidationError } from "../../../UI/ValidationError"
import * as urls from "../../../urls"
import { useThreadReplyContext } from "./ThreadReplyContext"
import ThreadReplyDialog from "./ThreadReplyDialog"
import ThreadReplyRootError from "./ThreadReplyRootError"
import usePostReplyMutation from "./usePostReplyMutation"

const Editor = React.lazy(() => import("../../../Editor"))

interface IThreadReplyNewFormProps {
  threadId: string
}

const ThreadReplyNewForm: React.FC<IThreadReplyNewFormProps> = ({
  threadId,
}) => {
  const { postMinLength } = useSettingsContext()
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
    <ThreadReplyDialog>
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
            <ThreadReplyRootError
              graphqlError={graphqlError}
              dataErrors={data?.postReply.errors}
            >
              {({ message }) => <PostingFormAlert>{message}</PostingFormAlert>}
            </ThreadReplyRootError>
            <React.Suspense fallback={<PostingFormLoader />}>
              <Field
                label={<Trans id="posting.message">Message contents</Trans>}
                name="markup"
                className="form-group-editor form-control-with-floating-error"
                input={
                  <Editor
                    submit={
                      <ButtonPrimary
                        text={
                          <Trans id="posting.submit_reply">Post reply</Trans>
                        }
                        loading={loading}
                        small
                      />
                    }
                  />
                }
                error={(error, value) => (
                  <ValidationError
                    error={error}
                    value={value.trim().length}
                    min={postMinLength}
                  >
                    {({ type, message }) => (
                      <FieldErrorFloating
                        key={context.form.formState.submitCount}
                        type={type}
                      >
                        {message}
                      </FieldErrorFloating>
                    )}
                  </ValidationError>
                )}
                labelReaderOnly
              />
            </React.Suspense>
          </form>
        </FormContext.Provider>
      </HookFormContext>
    </ThreadReplyDialog>
  )
}

export default ThreadReplyNewForm
