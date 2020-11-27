import { Trans } from "@lingui/macro"
import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext } from "../UI/Form"
import EditorBody from "./EditorBody"
import EditorButton from "./EditorButton"
import EditorMentions from "./EditorMentions"
import EditorPreview from "./EditorPreview"
import EditorPreviewButton from "./EditorPreviewButton"
import EditorTextarea from "./EditorTextarea"
import EditorToolbar from "./EditorToolbar"
import useSearchUsersQuery from "./useSearchUsersQuery"

interface IEditorProps {
  name?: string
  disabled?: boolean
  submit?: React.ReactNode
}

const Editor: React.FC<IEditorProps> = ({ name, disabled, submit }) => {
  const context = useFieldContext()
  const hookContext = useFormContext()
  const [preview, setPreview] = React.useState<string | null>(null)
  const searchUsers = useSearchUsersQuery()

  const finName = name || context.name

  if (!hookContext) return null
  if (!finName) return null

  const openPreview = () => {
    const value = hookContext.getValues(finName) || ""
    if (value.trim().length > 0) {
      setPreview(value.trim())
    }
  }

  const closePreview = () => setPreview(null)

  return (
    <EditorBody disabled={disabled || context.disabled}>
      {preview && <EditorPreview markup={preview} />}
      <EditorMentions>
        <EditorTextarea
          disabled={disabled || context.disabled}
          hidden={!!preview}
          invalid={context.invalid}
          name={finName}
          register={hookContext.register}
        />
      </EditorMentions>
      <EditorToolbar>
        <div className="row">
          <div className="col" />
          <div className="col-auto">
            {preview ? (
              <EditorButton
                disabled={disabled || context.disabled}
                onClick={closePreview}
              >
                <Trans id="editor.write">Write</Trans>
              </EditorButton>
            ) : (
              <EditorPreviewButton
                disabled={disabled || context.disabled}
                name={finName}
                onClick={openPreview}
              />
            )}
            {submit}
          </div>
        </div>
      </EditorToolbar>
    </EditorBody>
  )
}

export default Editor
