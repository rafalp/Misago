export default function ({ title, rank }) {
  return rank.is_tab || !!title || !!rank.title
}
