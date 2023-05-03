import cv2
import streamlit as st
import numpy as np
from PIL import Image
from streamlit_option_menu import option_menu
import face_detect
import face_recognition
import Chapter03 as ct3

st.set_page_config(page_title='Website xử lý ảnh', page_icon='assest/icon.png')

with st.sidebar:
    selected = option_menu(
        menu_title='Website Xử lý ảnh',
        options=['Phát hiện khuôn mặt', 'Nhận diện khuôn mặt', 'Xử lý ảnh'],
        styles={
            'nav-link': {'font-family': 'serif'}
        }
    )

if selected != 'Xử lý ảnh':
    st.title(selected)

if (selected == 'Phát hiện khuôn mặt'):
    face_detect.app()
elif (selected == 'Nhận diện khuôn mặt'):
    face_recognition.app()
else:
    chapters = ['Chương 3', 'Chương 4', 'Chương 5', 'Chương 9']
    chapter_contents = {
        'Chương 3': ['Làm âm ảnh (Negative)', 'Logarit ảnh', 'Lũy thừa ảnh', 'Biến đổi tuyến tính từng phần', 'Histogram', 'Cân bằng Histogram', 'Cân bằng Histogram ảnh màu', 'Local Histogram', 'Thống kê Histogram', 'Lọc box', 'Lọc Gauss', 'Phân ngưỡng', 'Lọc Median', 'Sharpen', 'Gradient'],
        'Chương 4': ['Spectrum', 'Lọc trong miền tần số - highpass filter', 'Vẽ bộ lọc Notch Reject', 'Xóa nhiễu moire'],
        'Chương 5': ['Tạo nhiễu chuyển động', 'Gỡ nhiễu của ảnh có ít nhiễu', 'Gỡ nhiễu của ảnh có nhiều nhiễu'],
        'Chương 9': ['Đếm thành phần liên thông', 'Đếm hạt gạo']
    }

    def content_on_change():
        st.session_state.file = False
    chapter = st.sidebar.selectbox(
        'Chọn chương', options=chapters, on_change=content_on_change)
    content = st.sidebar.selectbox(
        'Chọn nội dụng', options=chapter_contents[chapter], on_change=content_on_change)

    st.title(content)
    col1, col2 = st.columns(2)
    with col1:
        st.header("Ảnh gốc")

        def file_on_change():
            st.session_state.file = True

        orginal_container = st.empty()
        file = orginal_container.file_uploader(
            "Chọn ảnh", on_change=file_on_change)

        btn_col_1, btn_col_2 = st.columns([1, 4])
        with btn_col_1:
            button = st.button("Xử lý")
        with btn_col_2:
            reset = st.button("Reset")

    if file is not None:
        if button:
            with col2:
                st.header('Kết quả')
                image = Image.open(file)
                image_cv2 = np.array(image)

                if image_cv2.ndim == 3 and content != 'Cân bằng Histogram ảnh màu':
                    image_cv2 = cv2.cvtColor(image_cv2, cv2.COLOR_RGB2GRAY)
                if (content == 'Làm âm ảnh (Negative)'):
                    result = ct3.Negative(image_cv2)
                elif (content == 'Logarit ảnh'):
                    result = ct3.Logarit(image_cv2)
                elif (content == 'Lũy thừa ảnh'):
                    result = ct3.Power(image_cv2)
                elif (content == 'Biến đổi tuyến tính từng phần'):
                    result = ct3.PiecewiseLinear(image_cv2)
                elif (content == 'Histogram'):
                    result = ct3.Histogram(image_cv2)
                elif (content == 'Cân bằng Histogram'):
                    result = ct3.HistEqual(image_cv2)
                elif (content == 'Cân bằng Histogram ảnh màu'):
                    result = ct3.HistEqualColor(image_cv2)
                elif (content == 'Local Histogram'):
                    result = ct3.LocalHist(image_cv2)
                elif (content == 'Thống kê Histogram'):
                    result = ct3.HistStat(image_cv2)
                elif (content == 'Lọc box'):
                    result = ct3.BoxFilter(image_cv2)
                elif (content == 'Lọc Gauss'):
                    result = ct3.GaussFilter(image_cv2)
                elif (content == 'Phân ngưỡng'):
                    result = ct3.Threshold(image_cv2)
                elif (content == 'Lọc Median'):
                    result = ct3.MedianFilter(image_cv2)
                elif (content == 'Sharpen'):
                    result = ct3.Sharpen(image_cv2)
                elif (content == 'Gradient'):
                    result = ct3.Gradient(image_cv2)

                st.image(result, caption='Ảnh đã được xử lý')
        if reset:
            st.session_state.file = False

    # Xử lý ảnh
    with col1:
        if file is not None and st.session_state.get('file'):
            st.session_state.file = file
            img = Image.open(file)
            orginal_container.image(img, caption="Ảnh gốc")
