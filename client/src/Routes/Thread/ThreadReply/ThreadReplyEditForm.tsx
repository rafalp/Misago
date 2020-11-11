import { Trans } from "@lingui/macro"
import React from "react"
import { FormContext as HookFormContext } from "react-hook-form"
import { useSettingsContext, useToastsContext } from "../../../Context"
import { ButtonPrimary } from "../../../UI/Button"
import { Field, FieldErrorFloating, FormContext } from "../../../UI/Form"
import { PostingFormAlert, PostingFormLoader } from "../../../UI/PostingForm"
import { ValidationError } from "../../../UI/ValidationError"
import { IThreadReplyContext } from "./ThreadReplyContext"
import ThreadReplyDialog from "./ThreadReplyDialog"
import ThreadReplyRootError from "./ThreadReplyRootError"
import useEditPostMutation from "./useEditPostMutation"
import usePostMarkupQuery from "./usePostMarkupQuery"

const Editor = React.lazy(() => import("../../../Editor"))

interface IThreadReplyEditFormProps {
  context: IThreadReplyContext
  post: {
    id: string
  }
}

const ThreadReplyEditForm: React.FC<IThreadReplyEditFormProps> = ({
  context,
  post,
}) => {
  const { postMinLength } = useSettingsContext()
  const { showToast } = useToastsContext()
  const { cancelReply, form } = context
  const { setValue } = form

  const query = usePostMarkupQuery({ id: post.id })
  const mutation = useEditPostMutation(post)

  const defaultValue = query.data?.post?.markup || ""
  React.useEffect(() => {
    if (defaultValue.length) {
      console.log("SET VALUE!", defaultValue)
      setValue("markup", defaultValue)
    }
  }, [defaultValue])

  return (
    <ThreadReplyDialog>
      <React.Suspense fallback={<PostingFormLoader />}>
        {query.loading && (
          <>
            <PostingFormLoader />
            <Editor />
          </>
        )}
        {query.error && <div>ERROR</div>}
        {query.data?.post ? (
          <HookFormContext {...form}>
            <FormContext.Provider
              value={{ disabled: mutation.loading, id: "thread_post_edit" }}
            >
              <form
                onSubmit={form.handleSubmit(async (data, event) => {
                  if (mutation.loading) {
                    event?.preventDefault()
                    return
                  }

                  form.clearError()

                  try {
                    const result = await mutation.editPost(data.markup)
                    const { errors } = result.data?.editPost || {}

                    if (errors) {
                      errors?.forEach(({ location, type, message }) => {
                        const field = location.join(".") as "markup"
                        form.setError(field, type, message)
                      })
                    } else {
                      showToast(
                        <Trans id="edit_reply.message">
                          Reply has been edited.
                        </Trans>
                      )

                      cancelReply()
                    }
                  } catch (error) {
                    // do nothing when editPost throws
                    return
                  }
                })}
              >
                <ThreadReplyRootError
                  graphqlError={mutation.error}
                  dataErrors={mutation.data?.editPost.errors}
                >
                  {({ message }) => (
                    <PostingFormAlert>{message}</PostingFormAlert>
                  )}
                </ThreadReplyRootError>
                <Field
                  label={<Trans id="posting.message">Message contents</Trans>}
                  name="markup"
                  className="form-group-editor form-group-with-floating-error"
                  input={
                    <Editor
                      submit={
                        <ButtonPrimary
                          text={
                            <Trans id="posting.submit_changes">
                              Save changes
                            </Trans>
                          }
                          loading={mutation.loading}
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
              </form>
            </FormContext.Provider>
          </HookFormContext>
        ) : (
          <p>POST NOT FOUND</p>
        )}
      </React.Suspense>
    </ThreadReplyDialog>
  )
}

export default ThreadReplyEditForm
