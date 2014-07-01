import datetime

from django.utils.translation import ugettext_lazy as _
import pytz


TIMEZONES = (
    ('Pacific/Apia', _('(UTC-13:00) Samoa'), _('(UTC-14:00) Samoa')),
    ('Pacific/Midway', _('(UTC-11:00) Midway Islands, American Samoa')),
    ('Pacific/Honolulu', _('(UTC-10:00) Cook Islands, Hawaii, Society Islands')),
    ('America/Adak', _('(UTC-10:00) Aleutian Islands'), _('(UTC-09:00) Aleutian Islands')),
    ('Pacific/Marquesas', _('(UTC-09:30) Marquesas Islands')),
    ('Pacific/Gambier', _('(UTC-09:00) Gambier Islands')),
    ('America/Anchorage', _('(UTC-09:00) Alaska Standard Time'), _('(UTC-08:00) Alaska Daylight Time')),
    ('Pacific/Pitcairn', _('(UTC-08:00) Pitcairn Islands')),
    ('America/Los_Angeles', _('(UTC-08:00) Pacific Time (Canada and US)'), _('(UTC-07:00) Pacific Time (Canada and US)')),
    ('America/Santa_Isabel', _('(UTC-08:00) Baja California'), _('(UTC-07:00) Baja California')),
    ('America/Phoenix', _('(UTC-07:00) Mountain Standard Time (No DST)')),
    ('America/Hermosillo', _('(UTC-07:00) Sonora')),
    ('America/Denver', _('(UTC-07:00) Mountain Standard Time'), _('(UTC-06:00) Mountain Summer Time')),
    ('America/Chihuahua', _('(UTC-07:00) Baja California Sur, Chihuahua, Nayarit, Sinaloa'), _('(UTC-06:00) Baja California Sur, Chihuahua, Nayarit, Sinaloa')),
    ('America/Costa_Rica', _('(UTC-06:00) Costa Rica, El Salvador, Galapagos, Guatemala, Managua')),
    ('America/Chicago', _('(UTC-06:00) Central Standard Time'), _('(UTC-05:00) Central Daylight Time')),
    ('America/Mexico_City', _('(UTC-06:00) Mexican Central Zone'), _('(UTC-05:00) Mexican Central Zone')),
    ('America/Panama', _('(UTC-05:00) Bogota, Cayman, Guayaquil, Jamaica, Lima, Panama')),
    ('America/New_York', _('(UTC-05:00) Eastern Standard Time'), _('(UTC-04:00) Eastern Daylight Time')),
    ('America/Caracas', _('(UTC-04:30) Caracas')),
    ('America/Puerto_Rico', _('(UTC-04:00) Barbados, Dominica, Puerto Rico, Santo Domingo')),
    ('America/Santiago', _('(UTC-04:00) Bermuda, Campo Grande, Goose Bay, Santiago, Thule'), _('(UTC-03:00) Bermuda, Campo Grande, Goose Bay, Santiago, Thule')),
    ('America/St_Johns', _('(UTC-03:30) Newfoundland Time')),
    ('America/Argentina/La_Rioja', _('(UTC-03:00) San Juan, San Luis, Santa Cruz')),
    ('America/Sao_Paulo', _('(UTC-03:00) Buenos Aires, Godthab, Sao Paulo, Montevideo'), _('(UTC-02:00) Buenos Aires, Godthab, Sao Paulo, Montevideo')),
    ('America/Noronha', _('(UTC-02:00) Atlantic islands')),
    ('Atlantic/Cape_Verde', _('(UTC-01:00) Cape Verde Time')),
    ('Atlantic/Azores', _('(UTC-01:00) Azores, Scoresbysund'), _('(UTC) Azores, Scoresbysund')),
    ('utc', _('(UTC) Coordinated Universal Time')),
    ('Africa/Dakar', _('(UTC) Dakar, Rabat')),
    ('Europe/Lisbon', _('(UTC) Western European Time'), _('(UTC+01:00) Western European Summer Time')),
    ('Africa/Algiers', _('(UTC+01:00) West Africa Time')),
    ('Europe/Zurich', _('(UTC+01:00) Central European Time'), _('(UTC+02:00) Central European Summer Time')),
    ('Africa/Cairo', _('(UTC+02:00) Central Africa Time')),
    ('Europe/Athens', _('(UTC+02:00) Eastern European Time'), _('(UTC+03:00) Eastern European Summer Time')),
    ('Asia/Qatar', _('(UTC+03:00) East Africa Time')),
    ('Europe/Minsk', _('(UTC+03:00) Further-eastern European Time')),
    ('Asia/Tehran', _('(UTC+03:30) Iran Time'), _('(UTC+04:30) Iran Time')),
    ('Europe/Moscow', _('(UTC+04:00) Moscow Standard Time, Georgia Standard Time')),
    ('Asia/Dubai', _('(UTC+04:00) United Arab Emirates Standard Time')),
    ('Asia/Baku', _('(UTC+05:00) Baku, Yerevan'), _('(UTC+06:00) Baku, Yerevan')),
    ('Asia/Kabul', _('(UTC+04:30) Afghanistan Standard Time')),
    ('Asia/Karachi', _('(UTC+05:00) Ashgabat, Dushanbe, Karachi, Maldives, Tashkent')),
    ('Asia/Kolkata', _('(UTC+05:30) Colombo, Kolkata')),
    ('Asia/Kathmandu', _('(UTC+05:45) Kathmandu')),
    ('Asia/Almaty', _('(UTC+06:00) Astana, Bishkek, Dhaka, Thimphu, Yekaterinburg')),
    ('Asia/Rangoon', _('(UTC+06:30) Yangon, Cocos Islands')),
    ('Asia/Bangkok', _('(UTC+07:00) Bangkok, Ho Chi Minh, Jakarta, Novosibirsk')),
    ('Asia/Taipei', _('(UTC+08:00) Beijing, Hong Kong, Kuala Lumpur, Singapore, Taipei')),
    ('Australia/Perth', _('(UTC+08:00) Australian Western Standard Time')),
    ('Australia/Eucla', _('(UTC+08:45) Eucla Area')),
    ('Asia/Tokyo', _('(UTC+09:00) Tokyo, Seoul, Irkutsk, Pyongyang')),
    ('Australia/Darwin', _('(UTC+09:30) Australian Central Standard Time')),
    ('Australia/Adelaide', _('(UTC+09:30) Australian Central Standard Time')),
    ('Australia/Melbourne', _('(UTC+10:00) Australian Eastern Standard Time'), _('(UTC+11:00) Australian Eastern Summer Time')),
    ('Australia/Lord_Howe', _('(UTC+10:30) Lord Howe Island'), _('(UTC+11:00) Lord Howe Island')),
    ('Pacific/Guadalcanal', _('(UTC+11:00) Guadalcanal, Honiara, Noumea, Vladivostok')),
    ('Pacific/Norfolk', _('(UTC+11:30) Norfolk Island')),
    ('Pacific/Wake', _('(UTC+12:00) Kamchatka, Marshall Islands')),
    ('Pacific/Auckland', _('(UTC+12:00) Auckland, Fiji'), _('(UTC+13:00) Auckland, Fiji')),
    ('Pacific/Chatham', _('(UTC+12:45) Chatham Islands'), _('(UTC+13:45) Chatham Islands')),
    ('Pacific/Enderbury', _('(UTC+13:00) Phoenix Islands')),
    ('Pacific/Kiritimati', _('(UTC+14:00) Nuku\'alofa')),
)


def choices():
    """
    Generate user-friendly timezone list for selects
    """
    utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    ready_list = []
    for tz in TIMEZONES:
        if len(tz) == 3:
            tzinfo = pytz.timezone(tz[0])
            if utc_now.astimezone(tzinfo).dst().seconds > 0:
                ready_list.append((tz[0], tz[2]))
            else:
                ready_list.append((tz[0], tz[1]))
        else:
            ready_list.append(tz)

    return tuple(ready_list)
