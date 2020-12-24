import { useQuery } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { RichText } from "../types"

export const RICH_TEXT_PREVIEW_QUERY = gql`
  query RichTextPreview($markup: String!) {
    richText(markup: $markup)
  }
`

interface RichTextPreviewQueryData {
  richText: RichText
}

const useRichTextPreviewQuery = (markup: string) => {
  return useQuery<RichTextPreviewQueryData>(RICH_TEXT_PREVIEW_QUERY, {
    fetchPolicy: "network-only",
    variables: { markup },
  })
}

export default useRichTextPreviewQuery
