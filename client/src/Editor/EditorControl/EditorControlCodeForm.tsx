import { Trans, t } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { Field, FieldError, Form, FormFooter } from "../../UI/Form"
import Select from "../../UI/Select"
import { ModalFormBody, ModalFooter } from "../../UI/Modal"
import { ValidationError } from "../../UI/ValidationError"
import { EditorContextData } from "../EditorContext"

interface EditorControlCodeFormProps {
  context: EditorContextData
  close: () => void
}

interface FormValues {
  syntax: string
}

const AVAILABLE_SYNTAX = [
  "Bash",
  "C",
  "C++",
  "C#",
  "CSS",
  "Cython",
  "Elixir",
  "Erlang",
  "F#",
  "Haskell",
  "HTML",
  "Java",
  "JavaScript",
  "Kotlin",
  "Lua",
  "Matlab",
  "Pawn",
  "Perl",
  "PHP",
  "Python",
  "Ruby",
  "Rust",
  "Swift",
  "TypeScript",
]

const EditorControlCodeForm: React.FC<EditorControlCodeFormProps> = ({
  context,
  close,
}) => {
  const validators = Yup.object().shape({
    syntax: Yup.string(),
  })

  const choices = React.useMemo(() => {
    const choices = [
      {
        value: "",
        name: t({
          id: "editor.code_model.no_syntax",
          message: "No formatting",
        }),
      },
    ]

    AVAILABLE_SYNTAX.forEach((syntax) => {
      choices.push({
        value: syntax.toLowerCase(),
        name: syntax,
      })
    })

    return choices
  }, [])

  return (
    <Form<FormValues>
      id="editor_code_form"
      defaultValues={{ syntax: "" }}
      validators={validators}
      onSubmit={({ data: { syntax } }) => {
        context.replaceSelection({
          prefix: "\n\n```" + syntax + "\n",
          suffix: "\n```\n\n",
          default: t({
            id: "editor.code_default",
            message: "// Example code here",
          }),
          trim: true,
          lstrip: /\s+$/,
          rstrip: /^\s+/,
        })

        close()
      }}
    >
      <ModalFormBody>
        <Field
          label={
            <Trans id="editor.code_modal.syntax">Syntax formatting</Trans>
          }
          name="syntax"
          input={<Select options={choices} />}
          error={(error, value) => (
            <ValidationError error={error} value={value}>
              {({ message }) => <FieldError>{message}</FieldError>}
            </ValidationError>
          )}
        />
      </ModalFormBody>
      <ModalFooter>
        <FormFooter submitText={<Trans id="ok">Ok</Trans>} onCancel={close} />
      </ModalFooter>
    </Form>
  )
}

export default EditorControlCodeForm
