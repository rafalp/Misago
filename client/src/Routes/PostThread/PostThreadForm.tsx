import { Trans, t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { Redirect } from "react-router-dom"
import * as Yup from "yup"
import {
  useAuthContext,
  useSettingsContext,
  useToastsContext,
} from "../../Context"
import {
  Card,
  CardAlert,
  CardFooter,
  CardFormBody,
  CardHeader,
} from "../../UI/Card"
import { Checkbox } from "../../UI/Checkbox"
import { Field, FieldError, Form, FormFooter } from "../../UI/Form"
import Input from "../../UI/Input"
import RootError from "../../UI/RootError"
import {
  CategoryValidationError,
  ThreadTitleValidationError,
  ValidationError,
} from "../../UI/ValidationError"
import * as urls from "../../urls"
import { ICategoryChoice } from "./PostThread.types"
import PostThreadCategoryInput from "./PostThreadCategoryInput"
import usePostThreadMutation from "./usePostThreadMutation"

const Editor = React.lazy(() => import("../../Editor"))

interface IPostThreadFormProps {
  category?: string
  categories: Array<ICategoryChoice>
  validCategories: Array<string>
}

interface IPostThreadFormValues {
  category: string
  title: string
  markup: string
  isClosed: boolean
}

const PostThreadForm: React.FC<IPostThreadFormProps> = ({
  category,
  categories,
  validCategories,
}) => {
  const user = useAuthContext()
  const isModerator = user ? user.isModerator : false

  const { showToast } = useToastsContext()
  const {
    postBodyMinLength,
    threadTitleMaxLength,
    threadTitleMinLength,
  } = useSettingsContext()
  const [
    postThread,
    { data, loading, error: graphqlError },
  ] = usePostThreadMutation()

  const PostThreadSchema = Yup.object().shape({
    category: Yup.string().required("value_error.missing"),
    title: Yup.string()
      .required("value_error.thread_title.missing")
      .min(threadTitleMinLength, "value_error.any_str.min_length")
      .max(threadTitleMaxLength, "value_error.any_str.max_length")
      .matches(/[a-zA-Z0-9]/, "value_error.thread_title"),
    markup: Yup.string()
      .required("value_error.missing")
      .min(postBodyMinLength, "value_error.any_str.min_length"),
  })

  if (data?.postThread.thread) {
    return <Redirect to={urls.thread(data.postThread.thread)} />
  }

  return (
    <Card>
      <CardHeader
        title={<Trans id="post_thread.form">Post a new thread</Trans>}
      />
      <Form<IPostThreadFormValues>
        defaultValues={{
          category: category || "",
          title: "",
          markup: "",
          isClosed: false,
        }}
        disabled={loading}
        validationSchema={PostThreadSchema}
        onSubmit={async ({ clearError, setError, data: input }) => {
          clearError()

          const result = await postThread({ variables: { input } })
          const { errors, thread } = result.data?.postThread || {}

          errors?.forEach(({ location, type, message }) => {
            const field = location.join(".") as
              | "markup"
              | "title"
              | "category"
              | "isClosed"
            setError(field, type, message)
          })

          if (thread) {
            showToast(
              <Trans id="post_thread.message">
                New thread has been posted.
              </Trans>
            )
          }
        }}
      >
        <RootError
          graphqlError={graphqlError}
          dataErrors={data?.postThread.errors}
        >
          {({ message }) => <CardAlert>{message}</CardAlert>}
        </RootError>
        <CardFormBody>
          <Field
            label={<Trans id="post_thread.thread_title">Thread title</Trans>}
            name="title"
            input={
              <I18n>
                {({ i18n }) => (
                  <Input
                    placeholder={i18n._(
                      t("post_thread.thread_title")`Thread title`
                    )}
                  />
                )}
              </I18n>
            }
            error={(error, value) => (
              <ThreadTitleValidationError
                error={error}
                value={value.trim().length}
                min={threadTitleMinLength}
                max={threadTitleMaxLength}
              >
                {({ message }) => <FieldError>{message}</FieldError>}
              </ThreadTitleValidationError>
            )}
            labelReaderOnly
          />
          <Field
            label={
              <Trans id="post_thread.thread_category">Thread category</Trans>
            }
            name="category"
            input={
              <PostThreadCategoryInput
                choices={categories}
                validChoices={validCategories}
              />
            }
            error={(error) => (
              <CategoryValidationError error={error}>
                {({ message }) => <FieldError>{message}</FieldError>}
              </CategoryValidationError>
            )}
            labelReaderOnly
          />
          <Field
            label={
              <Trans id="post_thread.thread_message">Message contents</Trans>
            }
            name="markup"
            input={<Editor />}
            error={(error, value) => (
              <ValidationError
                error={error}
                value={value.trim().length}
                min={2}
                max={200}
              >
                {({ message }) => <FieldError>{message}</FieldError>}
              </ValidationError>
            )}
            labelReaderOnly
          />
          {isModerator && (
            <Field
              label={
                <Trans id="post_thread.close_thread">
                  Post thread as closed
                </Trans>
              }
              name="isClosed"
              input={<Checkbox />}
              error={(error) => (
                <ValidationError error={error}>
                  {({ message }) => <FieldError>{message}</FieldError>}
                </ValidationError>
              )}
              check
            />
          )}
        </CardFormBody>
        <CardFooter>
          <FormFooter
            submitText={<Trans id="post_thread.submit">Post thread</Trans>}
          />
        </CardFooter>
      </Form>
    </Card>
  )
}

export default PostThreadForm
