import PreloadStore from 'misago/services/preload-store';

export function local(datetime) {
  return datetime.utcOffset(PreloadStore.get('utcOffset') / 60);
}

export default function datetimeFormats() {
  return true;
}
