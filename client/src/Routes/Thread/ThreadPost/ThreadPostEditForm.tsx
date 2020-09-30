import { Trans, t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import * as Yup from "yup"
import { useSettingsContext } from "../../../Context"
import {
  ButtonPrimary,
  ButtonSecondary,
  CardAlert,
  CardBody,
  CardFooter,
  Form,
} from "../../../UI"
import { IPost } from "../Thread.types"
import ThreadPostLoader from "./ThreadPostLoader"
import ThreadPostRootError from "./ThreadPostRootError"
import useEditPostMutation from "./useEditPostMutation"
import usePostMarkupQuery from "./usePostMarkupQuery"

interface IThreadPostEditFormProps {
  post: IPost
  testLoading?: boolean
  close: () => void
}

interface IFormValues {
  markup: string
}

const Editor = React.lazy(() => import("../../../Editor"))

const ThreadPostEditForm: React.FC<IThreadPostEditFormProps> = ({
  testLoading,
  post,
  close,
}) => {
  const { postMinLength } = useSettingsContext()

  const EditThreadPostSchema = Yup.object().shape({
    markup: Yup.string()
      .required("value_error.missing")
      .min(postMinLength, "value_error.any_str.min_length"),
  })

  const query = usePostMarkupQuery({ id: post.id })
  const mutation = useEditPostMutation(post)

  if (testLoading) return <ThreadPostLoader />
  if (query.error || !query.data?.post) return <div>ERROR</div>

  return (
    <React.Suspense fallback={<ThreadPostLoader />}>
      {query.loading && (
        <>
          <ThreadPostLoader />
          <Editor name="markup" disabled={true} />
        </>
      )}
      <Form<IFormValues>
        className="post-edit-form"
        id={"thread_post_edit_form_" + post.id}
        defaultValues={{ markup: query.data.post.markup }}
        disabled={mutation.loading}
        validationSchema={EditThreadPostSchema}
        onSubmit={async ({ clearError, setError, data: { markup } }) => {
          clearError()

          try {
            const result = await mutation.editPost(markup)
            const { errors } = result.data?.editPost || {}

            if (errors) {
              errors?.forEach(({ location, type, message }) => {
                const field = location.join(".") as "markup"
                setError(field, type, message)
              })
            } else {
              close()
            }
          } catch (error) {
            // do nothing when editPost throws
            return
          }
        }}
      >
        <ThreadPostRootError
          graphqlError={mutation.error}
          dataErrors={mutation.data?.editPost.errors}
        >
          {({ message }) => <CardAlert>{message}</CardAlert>}
        </ThreadPostRootError>
        <CardBody className="post-edit-form-body">
          <Editor name="markup" disabled={mutation.loading} />
        </CardBody>
        <CardFooter className="post-edit-form-footer">
          <I18n>
            {({ i18n }) => (
              <ButtonSecondary
                text={<Trans id="cancel">Cancel</Trans>}
                disabled={mutation.loading}
                onClick={() => {
                  const confirm = window.confirm(
                    i18n._(
                      t(
                        "moderation.edit_post_cancel_prompt"
                      )`Are you sure you want to abandon changes?`
                    )
                  )
                  if (confirm) close()
                }}
                small
              />
            )}
          </I18n>
          <ButtonPrimary
            text={<Trans id="moderation.edit_post">Save changes</Trans>}
            loading={mutation.loading}
            small
          />
        </CardFooter>
      </Form>
    </React.Suspense>
  )
}

export default ThreadPostEditForm
