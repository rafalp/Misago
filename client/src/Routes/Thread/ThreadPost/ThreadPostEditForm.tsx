import { Trans, t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import * as Yup from "yup"
import {
  ButtonPrimary,
  ButtonSecondary,
  CardAlert,
  CardBody,
  CardFooter,
  Form,
  Textarea,
} from "../../../UI"
import { IPost } from "../Thread.types"
import ThreadPostRootError from "./ThreadPostRootError"
import useEditPostMutation from "./useEditPostMutation"

interface IThreadPostEditFormProps {
  post: IPost
  close: () => void
}

interface IFormValues {
  body: string
}

const ThreadPostEditForm: React.FC<IThreadPostEditFormProps> = ({
  post,
  close,
}) => {
  const EditThreadPostSchema = Yup.object().shape({
    body: Yup.string()
      .required("value_error.missing")
      .min(2, "value_error.any_str.min_length")
      .max(10000, "value_error.any_str.max_length"),
  })

  const { data, loading, editPost, error: graphqlError } = useEditPostMutation(
    post
  )

  return (
    <Form<IFormValues>
      id={"thread_post_edit_form_" + post.id}
      defaultValues={{ body: post.body.text }}
      disabled={loading}
      validationSchema={EditThreadPostSchema}
      onSubmit={async ({ clearError, setError, data: { body } }) => {
        clearError()

        try {
          const result = await editPost(body)
          const { errors } = result.data?.editPost || {}

          if (errors) {
            errors?.forEach(({ location, type, message }) => {
              const field = location.join(".")
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
        graphqlError={graphqlError}
        dataErrors={data?.editPost.errors}
      >
        {({ message }) => <CardAlert>{message}</CardAlert>}
      </ThreadPostRootError>
      <CardBody className="post-edit-form-body">
        <Textarea name="body" rows={7} />
      </CardBody>
      <CardFooter className="post-edit-form-footer">
        <I18n>
          {({ i18n }) => (
            <ButtonSecondary
              text={<Trans id="cancel">Cancel</Trans>}
              disabled={loading}
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
          loading={loading}
          small
        />
      </CardFooter>
    </Form>
  )
}

export default ThreadPostEditForm
