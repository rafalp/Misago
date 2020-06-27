export interface IPaginatorProps {
  page: number
  pages: number
  url: (page: number) => string
}
