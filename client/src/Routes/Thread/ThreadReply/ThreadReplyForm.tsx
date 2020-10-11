import { Trans } from "@lingui/macro"
import React from "react"
import { FormContext as HookFormContext } from "react-hook-form"
import { Redirect } from "react-router-dom"
import Editor from "../../../Editor"
import { useSettingsContext, useToastsContext } from "../../../Context"
import { ButtonPrimary } from "../../../UI/Button"
import { Field, FieldError, FormContext } from "../../../UI/Form"
import {
  PostingFormAlert,
  PostingFormBody,
  PostingFormDialog,
  PostingFormFooter,
  PostingFormHeader,
} from "../../../UI/PostingForm"
import RootError from "../../../UI/RootError"
import { ValidationError } from "../../../UI/ValidationError"
import * as urls from "../../../urls"
import { useThreadReplyContext } from "./ThreadReplyContext"
import usePostReplyMutation from "./usePostReplyMutation"

interface IThreadReplyFormProps {
  threadId: string
}

const ThreadReplyForm: React.FC<IThreadReplyFormProps> = ({ threadId }) => {
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

  const {
    form,
    fullscreen,
    minimized,
    mode,
    setFullscreen,
    setMinimized,
  } = context

  const isEditing = mode === "edit"

  return (
    <HookFormContext {...form}>
      <FormContext.Provider
        value={{ disabled: loading, id: "thread_post_reply" }}
      >
        <PostingFormDialog>
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
            <PostingFormHeader
              fullscreen={fullscreen}
              minimized={minimized}
              setFullscreen={setFullscreen}
              setMinimized={setMinimized}
            >
              {isEditing ? (
                <Trans id="posting.edit">Edit post</Trans>
              ) : (
                <Trans id="posting.reply">Reply thread</Trans>
              )}
            </PostingFormHeader>
            <RootError
              graphqlError={graphqlError}
              dataErrors={data?.postReply.errors}
            >
              {({ message }) => <PostingFormAlert>{message}</PostingFormAlert>}
            </RootError>
            <PostingFormBody>
              <Field
                label={<Trans id="posting.message">Message contents</Trans>}
                name="markup"
                className="form-group-editor"
                input={<Editor />}
                error={(error, value) => (
                  <ValidationError
                    error={error}
                    value={value.trim().length}
                    min={postMinLength}
                  >
                    {({ message }) => <FieldError>{message}</FieldError>}
                  </ValidationError>
                )}
                labelReaderOnly
              />
            </PostingFormBody>
            <PostingFormFooter>
              <ButtonPrimary
                text={
                  isEditing ? (
                    <Trans id="posting.submit_edit">Save changes</Trans>
                  ) : (
                    <Trans id="posting.submit_reply">Post reply</Trans>
                  )
                }
                loading={loading}
                small
              />
            </PostingFormFooter>
          </form>
        </PostingFormDialog>
      </FormContext.Provider>
    </HookFormContext>
  )
}

export default ThreadReplyForm
