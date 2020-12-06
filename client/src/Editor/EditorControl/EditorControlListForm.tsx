import { Trans, t } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { Field, FieldError, Form, FormFooter } from "../../UI/Form"
import { ModalFormBody, ModalFooter } from "../../UI/Modal"
import Select from "../../UI/Select"
import { ValidationError } from "../../UI/ValidationError"
import { IEditorContextValues } from "../EditorContext"
import EditorControlListInput from "./EditorControlListInput"

interface IEditorControlListFormProps {
  context: IEditorContextValues
  close: () => void
}

interface IFormValues {
  list: Array<string>
  type: string
}

const EditorControlListForm: React.FC<IEditorControlListFormProps> = ({
  context,
  close,
}) => {
  const validators = Yup.object().shape({
    list: Yup.array().of(Yup.string()).min(1),
    type: Yup.string(),
  })

  return (
    <Form<IFormValues>
      id="editor_list_form"
      defaultValues={{ list: [""], type: "ol" }}
      validators={validators}
      onSubmit={({ data: { list, type }, event }) => {
        const items = list
          .filter((item) => item.trim().length)
          .map((item, index) => {
            if (type === "ol") {
              return `${index + 1}. ${item.trim()}`
            }

            return `- ${item.trim()}`
          })

        if (items.length) {
          context.replaceSelection({
            prefix: "\n\n",
            suffix: "\n\n",
            replace: items.join("\n").trim(),
            lstrip: /\s+$/,
            rstrip: /^\s+/,
          })
        }

        event?.stopPropagation()
        close()
      }}
    >
      <ModalFormBody>
        <Field
          label={<Trans id="editor.list_modal.list">List items</Trans>}
          name="list"
          input={<EditorControlListInput />}
          error={(error, value) => (
            <ValidationError error={error} value={value}>
              {({ message }) => <FieldError>{message}</FieldError>}
            </ValidationError>
          )}
        />
        <Field
          label={<Trans id="editor.list_modal.type">List type</Trans>}
          name="type"
          input={
            <Select
              options={[
                {
                  value: "ol",
                  name: t({
                    id: "editor.list_modal.ordered",
                    message: "Ordered list (1., 2., 3.)",
                  }),
                },
                {
                  value: "ul",
                  name: t({
                    id: "editor.list_modal.unordered",
                    message: "Unordered list (-, -, -)",
                  }),
                },
              ]}
            />
          }
        />
      </ModalFormBody>
      <ModalFooter>
        <FormFooter submitText={<Trans id="ok">Ok</Trans>} onCancel={close} />
      </ModalFooter>
    </Form>
  )
}

export default EditorControlListForm
