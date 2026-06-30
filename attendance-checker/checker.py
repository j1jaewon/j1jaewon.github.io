from datetime import date, datetime, timedelta
import xlrd
import holidays

KR_HOLIDAYS = holidays.SouthKorea(years=range(2024, 2028))

EXTRA_COMPANY_HOLIDAYS: list[date] = []  # add company-specific days here


def is_holiday(d: date) -> bool:
    return d in KR_HOLIDAYS or d in EXTRA_COMPANY_HOLIDAYS


def is_special_day(d: date) -> bool:
    """토요일 or 공휴일/대체공휴일 → 특근 대상."""
    return d.weekday() == 5 or is_holiday(d)


def parse_time(t: str) -> timedelta:
    h, m, s = map(int, t.split(":"))
    return timedelta(hours=h, minutes=m, seconds=s)


def overlap_hours(start: timedelta, end: timedelta,
                  window_start: timedelta, window_end: timedelta) -> float:
    """Compute overlapping hours between two timedelta intervals (same-day reference)."""
    s = max(start, window_start)
    e = min(end, window_end)
    if e > s:
        return (e - s).total_seconds() / 3600
    return 0.0


def round_half(x: float) -> float:
    """Round to nearest 0.5."""
    return round(x * 2) / 2


# ---------------------------------------------------------------------------
# Shift classification
# ---------------------------------------------------------------------------

def classify_shift(checkin: timedelta, checkout: timedelta):
    """
    Returns 'day' or 'night'.
    Night shift: check-in >= 18:00 (20:00 nominal, but some flexibility).
    """
    return "night" if checkin >= timedelta(hours=18) else "day"


def calc_expected(work_date: date, checkin: timedelta, checkout_raw: timedelta,
                  crosses_midnight: bool):
    """
    Given a single shift, return dict of expected hour values.
    work_date = date on which 출근 was recorded.
    checkout_raw = time of day (timedelta from midnight) of 퇴근.
    crosses_midnight = True if 퇴근 is on the following calendar day.

    Rules:
    - Early check-in before shift start is ignored (clamped to shift start).
    - Early/on-time checkout without overtime is treated as shift end (17:00 / 05:00).
    - Overtime is calculated proportionally from shift end up to max (19:30 / 07:30).
    """
    shift = classify_shift(checkin, checkout_raw)
    special = is_special_day(work_date)

    checkout = checkout_raw + timedelta(days=1) if crosses_midnight else checkout_raw

    result = {
        "정취": 0.0,
        "잔업": 0.0,
        "특근": 0.0,
        "특근잔업": 0.0,
        "심야": 0.0,
    }

    if shift == "day":
        day_start  = timedelta(hours=8)
        day_end    = timedelta(hours=17)
        janup_end  = timedelta(hours=19, minutes=30)

        # Clamp checkin — early arrival doesn't count
        effective_checkin  = max(checkin, day_start)
        # Clamp checkout — leaving before/at 17:00 counts as 17:00
        effective_checkout = max(checkout, day_end)
        # Cap at max overtime end
        effective_checkout = min(effective_checkout, janup_end)

        overtime = max(timedelta(0), effective_checkout - day_end)

        if special:
            result["특근"] = 8.0
            result["특근잔업"] = round_half(overtime.total_seconds() / 3600)
        else:
            result["정취"] = 8.0
            result["잔업"] = round_half(overtime.total_seconds() / 3600)

    else:  # night shift: 20:00–05:00 regular, 05:00–07:30 잔업
        night_start = timedelta(hours=20)
        regular_end = timedelta(hours=29)        # 05:00 next day
        janup_end   = timedelta(hours=31, minutes=30)  # 07:30 next day
        simya_start = timedelta(hours=23)
        simya_end   = timedelta(hours=29, minutes=30)  # 05:30 next day

        effective_checkin  = max(checkin, night_start)
        effective_checkout = max(checkout, regular_end)
        effective_checkout = min(effective_checkout, janup_end)

        overtime = max(timedelta(0), effective_checkout - regular_end)

        if special:
            result["특근"] = 8.0
            result["특근잔업"] = round_half(overtime.total_seconds() / 3600)
        else:
            result["정취"] = 8.0
            result["잔업"] = round_half(overtime.total_seconds() / 3600)

        simya = overlap_hours(effective_checkin, effective_checkout, simya_start, simya_end)
        result["심야"] = round_half(simya)

    return result


# ---------------------------------------------------------------------------
# Parse raw tag log
# ---------------------------------------------------------------------------

def load_tag_log(filepath: str) -> dict:
    """
    Returns {name: [(date, time_str, mode), ...]} from Sheet1.
    """
    wb = xlrd.open_workbook(filepath)
    sh = wb.sheet_by_name("Sheet1")
    log: dict[str, list] = {}
    for r in range(1, sh.nrows):
        row = [sh.cell_value(r, c) for c in range(sh.ncols)]
        date_str, time_str, name, _, mode = row[0], row[1], row[2], row[3], row[4]
        if not name:
            continue
        log.setdefault(name, []).append((date_str, time_str, mode))
    return log


def pair_shifts(records: list) -> list[dict]:
    """
    Convert raw tag list for one employee into (work_date, checkin, checkout, crosses_midnight).
    Pairs 출근 → next 퇴근.
    """
    from collections import deque
    events = deque(records)
    shifts = []
    checkin_date = checkin_time = None

    while events:
        date_str, time_str, mode = events.popleft()
        t = parse_time(time_str)
        d = datetime.strptime(date_str, "%Y-%m-%d").date()

        if mode == "출근":
            checkin_date = d
            checkin_time = t
        elif mode == "퇴근" and checkin_date is not None:
            crosses = d > checkin_date
            shifts.append({
                "work_date": checkin_date,
                "checkin": checkin_time,
                "checkout": t,
                "crosses_midnight": crosses,
            })
            checkin_date = checkin_time = None

    return shifts


# ---------------------------------------------------------------------------
# Parse 근태현황
# ---------------------------------------------------------------------------

def load_attendance_sheet(filepath: str) -> dict:
    """
    Returns {name: {day: {항목: value}}} from 보광 sheet.

    Row structure per employee (9 rows per block):
      +0  col0=NO, col1=dept, col3='정취 / 주휴'     ← 정취 data
      +1  col1=name, col3='연장', col4='잔업시간'    ← 잔업 data
      +2  col4='중식,석식'
      +3  col4='특근시간'
      +4  col4='특근잔업'
      +5  col4='심야시간'
      +6  col4='지 각'
      +7  col4='조퇴.외출'
      +8  col1='구            분'
    """
    wb = xlrd.open_workbook(filepath)
    sh = wb.sheet_by_name("보광")

    DAY_COL_OFFSET = 5  # col index where day 1 starts

    SKIP_NAMES = {"성   명", "구            분", "소속명", "생산", "사무", "품질",
                  "세척검사", "조장", "물자", "반장", ""}

    def read_day_values(row) -> dict:
        vals = {}
        for day in range(1, 32):
            col = DAY_COL_OFFSET + (day - 1)
            if col < len(row):
                v = row[col]
                if isinstance(v, float) and v > 0:
                    vals[day] = v
        return vals

    result: dict[str, dict] = {}

    for r in range(6, sh.nrows):
        row = [sh.cell_value(r, c) for c in range(sh.ncols)]
        # Block start: col0 is a number (employee NO), col3 == '정취 / 주휴'
        if isinstance(row[0], float) and row[0] > 0 and str(row[3]).strip() == "정취 / 주휴":
            # name is one row below in col1
            if r + 1 >= sh.nrows:
                continue
            name_row = [sh.cell_value(r + 1, c) for c in range(sh.ncols)]
            name = str(name_row[1]).strip()
            if not name or name in SKIP_NAMES:
                continue

            items: dict[str, dict] = {
                "정취":    read_day_values(row),
                "잔업":    read_day_values(name_row),
            }

            # Rows +2 to +5 for remaining items
            item_labels = {
                "중식,석식": None,
                "특근시간":  "특근",
                "특근잔업":  "특근잔업",
                "심야시간":  "심야",
            }
            for offset in range(2, 7):
                if r + offset >= sh.nrows:
                    break
                sub = [sh.cell_value(r + offset, c) for c in range(sh.ncols)]
                label = str(sub[4]).strip()
                if label in item_labels and item_labels[label]:
                    items[item_labels[label]] = read_day_values(sub)

            # Transpose to {day: {item: val}}
            by_day: dict[int, dict] = {}
            for key, day_vals in items.items():
                for day, val in day_vals.items():
                    by_day.setdefault(day, {})[key] = val

            result[name] = by_day

    return result


# ---------------------------------------------------------------------------
# Main verification
# ---------------------------------------------------------------------------

def verify(tag_filepath: str, attendance_filepath: str) -> list[dict]:
    tag_log = load_tag_log(tag_filepath)
    attendance = load_attendance_sheet(attendance_filepath)

    issues = []
    summaries = []

    for name, records in tag_log.items():
        if name not in attendance:
            continue

        shifts = pair_shifts(records)
        expected_by_day: dict[int, dict] = {}

        for s in shifts:
            d = s["work_date"]
            exp = calc_expected(d, s["checkin"], s["checkout"], s["crosses_midnight"])
            day_num = d.day
            # Accumulate (multiple shifts same day unlikely but safe)
            if day_num not in expected_by_day:
                expected_by_day[day_num] = exp
            else:
                for k in exp:
                    expected_by_day[day_num][k] = expected_by_day[day_num].get(k, 0) + exp[k]

        recorded = attendance[name]
        employee_issues = []
        day_details = []

        # Only verify days where tag data exists.
        # Days with no tag (Sundays, 주휴, 연차, holidays) may still have
        # legitimate 8h in 정취/주휴 column — we cannot verify those.
        all_days = sorted(set(list(expected_by_day.keys()) + list(recorded.keys())))
        for day in all_days:
            if day not in expected_by_day:
                continue  # no tag data → skip
            exp = expected_by_day.get(day, {})
            rec = recorded.get(day, {})
            KEY_MAP = {
                "정취": "정취",
                "잔업": "잔업",
                "특근": "특근",
                "특근잔업": "특근잔업",
                "심야": "심야",
            }
            day_issues = []
            for exp_key, rec_key in KEY_MAP.items():
                e_val = round_half(exp.get(exp_key, 0.0))
                r_val = rec.get(rec_key, 0.0)
                if abs(e_val - r_val) >= 0.5:
                    day_issues.append({
                        "항목": exp_key,
                        "기록값": r_val,
                        "계산값": e_val,
                        "차이": r_val - e_val,
                    })

            day_details.append({
                "day": day,
                "expected": exp,
                "recorded": rec,
                "issues": day_issues,
            })
            employee_issues.extend([{**i, "day": day} for i in day_issues])

        summaries.append({
            "name": name,
            "issues": employee_issues,
            "days": day_details,
            "issue_count": len(employee_issues),
        })

    summaries.sort(key=lambda x: -x["issue_count"])
    return summaries
