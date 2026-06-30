import tempfile
import pandas as pd
import streamlit as st
from checker import verify

st.set_page_config(page_title="근태 검증 대시보드", page_icon="🕐", layout="wide")

st.title("🕐 근태 검증 대시보드")
st.caption("태그 로그와 근태현황을 업로드하면 불일치 항목을 자동으로 찾아드립니다.")

col1, col2 = st.columns(2)
with col1:
    tag_file = st.file_uploader("📂 태그 로그 파일 (출퇴근 기계 원본)", type=["xls", "xlsx"])
with col2:
    att_file = st.file_uploader("📋 근태현황 파일 (중간관리자 기입)", type=["xls", "xlsx"])

if tag_file and att_file:
    with st.spinner("분석 중..."):
        with tempfile.NamedTemporaryFile(suffix=".xls", delete=False) as tf:
            tf.write(tag_file.read())
            tag_path = tf.name
        with tempfile.NamedTemporaryFile(suffix=".xls", delete=False) as af:
            af.write(att_file.read())
            att_path = af.name

        results = verify(tag_path, att_path)

    # ── Summary metrics ──
    total = len(results)
    issue_count = sum(1 for r in results if r["issue_count"] > 0)
    total_issues = sum(r["issue_count"] for r in results)

    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("검증 대상 직원", total)
    m2.metric("오류 발견 직원", issue_count, delta=None)
    m3.metric("정상 직원", total - issue_count)
    m4.metric("총 불일치 항목", total_issues)

    st.divider()

    ITEMS = ["정취", "잔업", "특근", "특근잔업", "심야"]

    # ── Filter ──
    show_only_issues = st.toggle("오류 있는 직원만 보기", value=True)

    for emp in results:
        if show_only_issues and emp["issue_count"] == 0:
            continue

        label = f"⚠️ {emp['name']} — 오류 {emp['issue_count']}건" if emp["issue_count"] > 0 else f"✅ {emp['name']} — 정상"
        with st.expander(label, expanded=(emp["issue_count"] > 0)):
            rows = []
            for d in emp["days"]:
                row = {"날짜": f"{d['day']}일"}
                has_issue = bool(d["issues"])
                issue_items = {i["항목"] for i in d["issues"]}
                for item in ITEMS:
                    rec = d["recorded"].get(item, 0)
                    exp = d["expected"].get(item, 0)
                    if item in issue_items:
                        row[item] = f"🔴 {rec}h → {exp}h"
                    elif rec == 0 and exp == 0:
                        row[item] = "-"
                    else:
                        row[item] = f"{rec}h"
                rows.append(row)

            df = pd.DataFrame(rows).set_index("날짜")
            st.dataframe(df, use_container_width=True)
