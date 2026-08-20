#!/usr/bin/env bash
set -u
BASE="https://dd-engine1.vercel.app/api/duyen-dich/analyze"
OUT="/home/ubuntu/dd_engine1/live_cases_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
cat > "$OUT/cases.tsv" <<'CASES'
case_01	369147	tình cảm hiện tại nên quan sát điều gì?
case_02	428615	công việc và hướng ưu tiên trong tháng này
case_03	751204	có nên ký hợp đồng mới không?
case_04	196438	dự án đang chậm cần xử lý thế nào?
case_05	583920	chuyến đi sắp tới cần lưu ý gì?
CASES
printf 'case\ttotal\tstatus\tseconds\tfile\n' > "$OUT/results.tsv"
while IFS=$'\t' read -r case_id total question; do
  [ -z "$case_id" ] && continue
  payload=$(printf '{"mode":"mot_tin_hieu","total":%s,"question":"%s"}' "$total" "$question")
  output="$OUT/${case_id}.json"
  status_file="$OUT/${case_id}.status"
  status=$(curl -sS --max-time 130 -o "$output" -w '%{http_code} %{time_total}' -X POST "$BASE" -H 'Content-Type: application/json' --data "$payload" 2>"$OUT/${case_id}.stderr" || printf '000 130')
  code=${status%% *}
  seconds=${status#* }
  printf '%s\t%s\t%s\t%s\t%s\n' "$case_id" "$total" "$code" "$seconds" "$output" >> "$OUT/results.tsv"
  printf '%s\n' "$status" > "$status_file"
done < "$OUT/cases.tsv"
printf '%s\n' "$OUT"
cat "$OUT/results.tsv"
