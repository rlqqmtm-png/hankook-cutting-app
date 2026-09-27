import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="한국컷팅 퀵 배차 시스템", page_icon="🚚", layout="centered")

st.markdown("### 🚚 한국컷팅 스마트 퀵 배차 관리 시스템")

# 1. 거래처 기본 DB
if 'clients_db' not in st.session_state:
    st.session_state.clients_db = {
        "구찌 청담 플래그십": {
            "주소": "서울 강남구 압구정로 462",
            "담당자": [
                {"이름": "김구찌 매니저", "연락처": "010-1234-5678"},
                {"이름": "박구찌 부점장", "연락처": "010-9999-8888"}
            ]
        },
        "디올 성수 콘셉트스토어": {
            "주소": "서울 성동구 연무장5길 7",
            "담당자": [
                {"이름": "이디올 팀장", "연락처": "010-9876-5432"},
                {"이름": "최디올 매니저", "연락처": "010-1111-2222"}
            ]
        },
        "루이비통 롯데잠실점": {
            "주소": "서울 송파구 올림픽로 300",
            "담당자": [
                {"이름": "한루이 실장", "연락처": "010-3333-4444"},
                {"이름": "정루이 매니저", "연락처": "010-5555-6666"}
            ]
        },
        "아디다스 강남 브랜드센터": {
            "주소": "서울 강남구 강남대로 470",
            "담당자": [
                {"이름": "최아디 팀장", "연락처": "010-6666-7777"}
            ]
        },
        "Apple 가로수길": {
            "주소": "서울 강남구 가로수길 43",
            "담당자": [
                {"이름": "이애플 스페셜리스트", "연락처": "010-8888-9999"}
            ]
        }
    }

# 2. 주문 내역 세션
if 'shared_history' not in st.session_state:
    st.session_state.shared_history = [
        {
            "주문ID": "ORD-001",
            "시간": "2026-06-07 10:30",
            "거래처": "구찌 청담 플래그십",
            "주소": "서울 강남구 압구정로 462",
            "담당자": "김구찌 매니저",
            "연락처": "010-1234-5678",
            "품목": "외관 대형 타일 세트",
            "차량": "1톤 트럭 (대형 출력물)",
            "상태": "접수완료",
            "특이사항": "파손 주의"
        }
    ]

# 거래처 변경 콜백 함수
def update_client_selection():
    selected = st.session_state.selected_client_key
    st.session_state.input_addr_val = st.session_state.clients_db[selected]["주소"]
    mgrs = st.session_state.clients_db[selected]["담당자"]
    st.session_state.selected_mgr_key = mgrs[0]["이름"]
    st.session_state.input_mgr_name_val = mgrs[0]["이름"]
    st.session_state.input_mgr_phone_val = mgrs[0]["연락처"]

# 담당자 변경 콜백 함수
def update_mgr_selection():
    selected_client = st.session_state.selected_client_key
    selected_mgr = st.session_state.selected_mgr_key
    if selected_mgr == "+ 신규 담당자 직접 입력":
        st.session_state.input_mgr_name_val = ""
        st.session_state.input_mgr_phone_val = ""
    else:
        mgrs = st.session_state.clients_db[selected_client]["담당자"]
        matched = next((m for m in mgrs if m["이름"] == selected_mgr), None)
        if matched:
            st.session_state.input_mgr_name_val = matched["이름"]
            st.session_state.input_mgr_phone_val = matched["연락처"]

tab1, tab2 = st.tabs(["📝 신규 주문 등록", "📋 주문 내역 관리 및 상태 변경"])

with tab1:
    st.markdown("#### 새로운 퀵 배차 주문 접수")
    client_mode = st.radio("거래처 구분", ["등록된 기존 거래처", "신규 거래처 직접 입력"], horizontal=True)

    if client_mode == "등록된 기존 거래처":
        clients_list = list(st.session_state.clients_db.keys())
        if 'selected_client_key' not in st.session_state or st.session_state.selected_client_key not in clients_list:
            st.session_state.selected_client_key = clients_list[0]
            st.session_state.input_addr_val = st.session_state.clients_db[clients_list[0]]["주소"]
            st.session_state.selected_mgr_key = st.session_state.clients_db[clients_list[0]]["담당자"][0]["이름"]
            st.session_state.input_mgr_name_val = st.session_state.clients_db[clients_list[0]]["담당자"][0]["이름"]
            st.session_state.input_mgr_phone_val = st.session_state.clients_db[clients_list[0]]["담당자"][0]["연락처"]

        st.selectbox("거래처(매장) 선택", clients_list, key="selected_client_key", on_change=update_client_selection)
        st.text_input("목적지 주소", key="input_addr_val")

        curr_client = st.session_state.selected_client_key
        mgr_options = [m["이름"] for m in st.session_state.clients_db[curr_client]["담당자"]] + ["+ 신규 담당자 직접 입력"]
        
        st.selectbox("현장 담당자 선택", mgr_options, key="selected_mgr_key", on_change=update_mgr_selection)
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("담당자 성함", key="input_mgr_name_val")
        with col2:
            st.text_input("담당자 연락처", key="input_mgr_phone_val")

        final_client_name = st.session_state.selected_client_key
        final_address = st.session_state.input_addr_val
        final_mgr_name = st.session_state.input_mgr_name_val
        final_mgr_phone = st.session_state.input_mgr_phone_val

    else:
        final_client_name = st.text_input("신규 거래처(현장) 이름", placeholder="예: 샤넬 명동 플래그십")
        col_a, col_b = st.columns([2, 1])
        with col_a:
            new_addr_base = st.text_input("도로명 주소", placeholder="예: 서울 중구 남대문로 81")
        with col_b:
            new_addr_detail = st.text_input("상세 위치", placeholder="예: 3층 행사장 앞")
        final_address = f"{new_addr_base} {new_addr_detail}".strip()

        col1, col2 = st.columns(2)
        with col1:
            final_mgr_name = st.text_input("현장 담당자 이름", placeholder="모르면 비워두세요")
        with col2:
            final_mgr_phone = st.text_input("담당자 연락처", placeholder="모르면 비워두세요")

    st.markdown("---")
    item_name = st.text_input("출력물 / 제품 품목 (필수)", placeholder="예: 구찌 외관 대형 타일 세트 (3pcs)")
    vehicle_type = st.selectbox(
        "배차 차량 선택",
        ["오토바이 (소형)", "다마스 (중형)", "라보 (부피 자재)", "1톤 트럭 (대형 출력물)"]
    )
    memo = st.text_area("특이사항 및 전달 메모", placeholder="예: 지하 2층 화물엘리베이터 앞 하차 요망, 파손 주의")

    if st.button("🚀 접수요청 등록하기", type="primary", use_container_width=True):
        if not final_client_name or not item_name:
            st.error("거래처 이름과 제품 품목은 반드시 입력해야 합니다!")
        else:
            new_id = f"ORD-{len(st.session_state.shared_history) + 1:03d}"
            new_record = {
                "주문ID": new_id,
                "시간": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "거래처": final_client_name,
                "주소": final_address if final_address else "주소 미입력",
                "담당자": final_mgr_name if final_mgr_name else "미정",
                "연락처": final_mgr_phone if final_mgr_phone else "미정",
                "품목": item_name,
                "차량": vehicle_type,
                "상태": "접수요청",
                "특이사항": memo
            }
            st.session_state.shared_history.insert(0, new_record)

            if client_mode == "신규 거래처 직접 입력" and final_client_name not in st.session_state.clients_db:
                st.session_state.clients_db[final_client_name] = {
                    "주소": final_address,
                    "담당자": [{"이름": final_mgr_name, "연락처": final_mgr_phone}] if final_mgr_name else []
                }
            elif client_mode == "등록된 기존 거래처" and st.session_state.selected_mgr_key == "+ 신규 담당자 직접 입력" and final_mgr_name:
                st.session_state.clients_db[final_client_name]["담당자"].append(
                    {"이름": final_mgr_name, "연락처": final_mgr_phone}
                )

            st.success(f"[{new_id}] 접수요청이 등록되었습니다!")
            
            st.markdown("##### 📋 [기사님 전달용 문자 양식]")
            sms_text = f"""[한국컷팅 배차 지시]
- 현장명: {final_client_name}
- 목적지: {final_address}
- 담당자: {final_mgr_name} ({final_mgr_phone})
- 차량: {vehicle_type}
- 물품: {item_name}
- 특이사항: {memo if memo else '없음'}"""
            st.code(sms_text, language="text")

with tab2:
    st.markdown("#### 전체 주문 현황 및 4단계 상태 관리")
    
    status_filter = st.radio("진행 단계 필터", ["전체보기", "📝 접수요청", "📥 접수완료", "🚚 배송중", "✅ 배송완료"], horizontal=True)

    history = st.session_state.shared_history
    if not history:
        st.info("등록된 주문 내역이 없습니다.")
    else:
        for idx, item in enumerate(history):
            if status_filter != "전체보기" and item["상태"] not in status_filter:
                continue

            with st.expander(f"[{item['상태']}] {item['주문ID']} | {item['거래처']} - {item['품목']} ({item['시간']})", expanded=(item['상태'] in ["접수요청", "접수완료"])):
                st.write(f"📍 **배송지 주소:** {item['주소']}")
                st.write(f"👤 **현장 담당자:** {item['담당자']} ({item['연락처']})")
                st.write(f"🚚 **배차 차량:** {item['차량']}")
                if item['특이사항']:
                    st.write(f"📝 **메모:** {item['특이사항']}")

                st.markdown("**진행 상태 변경:**")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    if st.button("접수요청", key=f"btn1_{idx}"):
                        item["상태"] = "접수요청"
                        st.rerun()
                with c2:
                    if st.button("접수완료", key=f"btn2_{idx}"):
                        item["상태"] = "접수완료"
                        st.rerun()
                with c3:
                    if st.button("배송중", key=f"btn3_{idx}"):
                        item["상태"] = "배송중"
                        st.rerun()
                with c4:
                    if st.button("배송완료", key=f"btn4_{idx}"):
                        item["상태"] = "배송완료"
                        st.rerun()