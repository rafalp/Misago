import React from "react"
import RichText from "../UI/RichText"
import EditorPreviewError from "./EditorPreviewError"
import EditorPreviewLoader from "./EditorPreviewLoader"
import useRichTextPreviewQuery from "./useRichTextPreviewQuery"

interface IEditorPreviewProps {
  markup: string
}

const EditorPreview: React.FC<IEditorPreviewProps> = ({ markup }) => {
  const { data, loading, error } = useRichTextPreviewQuery(markup)

  if (loading) return <EditorPreviewLoader />
  if (error) return <EditorPreviewError error={error} />

  return (
    <div className="form-editor-preview">
      {data && <RichText richText={data.richText} />}
    </div>
  )
}

export default EditorPreview
