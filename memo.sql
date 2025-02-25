WITH stats AS (
  SELECT
    COUNT(CASE WHEN sleep_hours >= 7 THEN 1 END) AS slept_days, -- 7時間以上の睡眠日数
    COUNT(CASE WHEN sleep_start_utc < DATE_FORMAT(sleep_start_utc, '%Y-%m-%d 14:00:00') THEN 1 END) AS early_sleep_days, -- 14時前に寝た日数
    COUNT(CASE WHEN sleep_end_utc >= DATE_FORMAT(sleep_end_utc, '%Y-%m-%d 22:00:00') THEN 1 END) AS early_wake_days -- 22時後に起きた日数
  FROM daily.garmin
  WHERE date >= DATE_FORMAT(UTC_TIMESTAMP(), '%Y-%m-01')  
    AND date < DATE_FORMAT(UTC_TIMESTAMP() + INTERVAL 1 MONTH, '%Y-%m-%d')
    AND (sleep_hours IS NOT NULL AND sleep_start_utc IS NOT NULL AND sleep_end_utc IS NOT NULL)
),
bath_stats AS (
  SELECT
    COUNT(CASE WHEN is_bathed = 1 THEN 1 END) AS bathed_days -- 入浴した日数
  FROM daily.daily_logs
  WHERE date >= DATE_FORMAT(UTC_TIMESTAMP(), '%Y-%m-01')  
    AND date < DATE_FORMAT(UTC_TIMESTAMP() + INTERVAL 1 MONTH, '%Y-%m-%d')
    AND is_bathed IS NOT NULL
),
remaining AS (
  SELECT
  DAY(LAST_DAY(CURRENT_DATE)) AS total_days, -- 今月の日数
  DATEDIFF(LAST_DAY(UTC_TIMESTAMP()), UTC_TIMESTAMP()) + 1 AS remaining_days, -- 今月の残り日数
  DAY(CURRENT_DATE) AS current_day_of_month
)
SELECT
-- floor(今月の日数-(今月の日数*目標入浴率))-(今日の日数-入浴した数)

--   slept_days as 爆睡回数,
--   total_days as total_days,
--   current_day_of_month as current_day_of_month,
--   bathed_days as bathed_days,
--   total_days * 0.9 as mokuhyou,
  FLOOR(total_days-(total_days * 0.9)) - (current_day_of_month - bathed_days) AS 入浴サボれる回数,

  FLOOR(total_days-(total_days * 0.7)) - (current_day_of_month - early_sleep_days) AS 早寝サボれる回数,

  FLOOR(total_days-(total_days * 0.8)) - (current_day_of_month - slept_days) AS 爆睡サボれる回数,

  FLOOR(total_days-(total_days * 0.7)) - (current_day_of_month - early_wake_days) AS 早起きサボれる回数,

  -- 今月の残り日数
  remaining_days
FROM stats, bath_stats, remaining;