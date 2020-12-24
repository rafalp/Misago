export interface PaginatorProps {
  page: number
  pages: number
  url: (page: number) => string
}
