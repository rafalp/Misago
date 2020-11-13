import { Trans } from "@lingui/macro"
import React from "react"
import { FormProvider as HookFormProvider } from "react-hook-form"
import { useSettingsContext, useToastsContext } from "../../../Context"
import { ButtonPrimary } from "../../../UI/Button"
import { Field, FieldErrorFloating, FormContext } from "../../../UI/Form"
import { PostingFormAlert, PostingFormLoader } from "../../../UI/PostingForm"
import { ValidationError } from "../../../UI/ValidationError"
import ThreadPostRootError from "../ThreadPostRootError"
import { IThreadReplyContext } from "./ThreadReplyContext"
import ThreadReplyDialog from "./ThreadReplyDialog"
import ThreadReplyEditError from "./ThreadReplyEditError"
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
  const { cancelReply, form, setValue } = context

  const query = usePostMarkupQuery({ id: post.id })
  const mutation = useEditPostMutation(post)

  const defaultValue = query.data?.post?.markup || ""
  React.useEffect(() => {
    if (defaultValue.length) {
      setValue(defaultValue)
    }
  }, [setValue, defaultValue])

  if (query.loading) {
    return (
      <ThreadReplyDialog>
        <React.Suspense fallback={<PostingFormLoader />}>
          <PostingFormLoader />
          <Editor />
        </React.Suspense>
      </ThreadReplyDialog>
    )
  }

  if (query.error) {
    return <ThreadReplyEditError error={query.error} />
  }

  if (!query.data?.post) {
    return <ThreadReplyEditError />
  }

  return (
    <ThreadReplyDialog>
      <React.Suspense fallback={<PostingFormLoader />}>
        <HookFormProvider {...form}>
          <FormContext.Provider
            value={{ disabled: mutation.loading, id: "thread_post_edit" }}
          >
            <form
              onSubmit={form.handleSubmit(async (data, event) => {
                if (mutation.loading) {
                  event?.preventDefault()
                  return
                }

                form.clearErrors()

                try {
                  const result = await mutation.editPost(data.markup)
                  const { errors } = result.data?.editPost || {}

                  if (errors) {
                    errors?.forEach(({ location, type, message }) => {
                      const field = location.join(".") as "markup"
                      form.setError(field, { type, message })
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
              <ThreadPostRootError
                graphqlError={mutation.error}
                dataErrors={mutation.data?.editPost.errors}
              >
                {({ message }) => (
                  <PostingFormAlert>{message}</PostingFormAlert>
                )}
              </ThreadPostRootError>
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
        </HookFormProvider>
      </React.Suspense>
    </ThreadReplyDialog>
  )
}

export default ThreadReplyEditForm
