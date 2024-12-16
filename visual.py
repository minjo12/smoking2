from flask import Flask, render_template, url_for
import random
import folium
from folium.plugins import MarkerCluster as MC
import pandas as pd
import json

def show_smoking():
    # CSV 파일을 읽어와 데이터프레임(sd)로 저장 (UTF-8 인코딩, 쉼표로 구분된 파일)
    sd = pd.read_csv('static/smoking.csv', encoding='utf-8', sep=',')

    # 서울시 구별 GeoJSON 파일을 불러옴 (지역 경계 데이터)
    seoul_gu = json.load(open('static/seoul_gu.json', encoding='utf-8'))

    # 지도 객체 생성 (중심 좌표: 서울 시청, 줌 레벨: 11)
    map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)


    # GeoJSON 데이터를 지도 위에 표시 (서울 구별 경계선 스타일 적용)
    folium.GeoJson(
        seoul_gu,
        style_function=lambda x: {
            'fillColor': 'blue',  # 채우기 색상: 파란색
            'color': 'black',     # 경계선 색상: 검정색
            'weight': 2,          # 경계선 두께: 2
            'fillOpacity': 0.1    # 채우기 투명도: 10%
        }
    ).add_to(map)  # 지도에 추가

    # 마커 클러스터링 객체 생성 (마커를 그룹화하여 지도 혼잡도를 줄임)
    mc = MC().add_to(map)

    icon_path = "static/smoking-area.png"

    # 데이터프레임의 각 행을 반복 처리
    for i, r in sd.iterrows():
        # 현재 행에서 데이터를 읽어옴
        nm = r['시설형태'] if pd.notna(r['시설형태']) else '알 수 없음'
        ad = r['설치 위치'] if pd.notna(r['설치 위치']) else '알 수 없음'
        te = r['데이터기준일'] if pd.notna(r['데이터기준일']) else '알 수 없음'  
        lo = r['위도']
        la = r['경도']

        # 팝업에 표시할 HTML 내용 생성
        ps = f'<b>시설형태:{nm}</b><br>설치 위치:{ad}<br>데이터기준일:{te}<br>'

        custom_icon = folium.CustomIcon(
            icon_path,
            icon_size=(40, 40)  # 아이콘 크기 조정
        )
            # 지도에 추가할 마커 생성 (위도, 경도로 위치 지정)
        mk = folium.Marker(
            [lo, la],  # 마커 위치
            popup=folium.Popup(ps, max_width=400),
            icon=custom_icon
        )
            # 마커를 클러스터에 추가
        mk.add_to(mc)

    # 지도 HTML 렌더링하여 반환 (Flask 뷰에서 사용)
    return map.get_root().render()

