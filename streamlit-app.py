import tempfile
import cv2
import streamlit as st
import PIL
from ultralytics import YOLO


def image_input(confidence):
	
	source_img = st.sidebar.file_uploader("Загрузите картинку", type=['png', 'jpeg', 'jpg'])
	
	DEFAULT_image = '1.jpg'

	if not source_img:
		uploaded_image = DEFAULT_image
	else:
		try:
			uploaded_image = PIL.Image.open(source_img)
		except Exception as ex:
			st.error("Ошибка открытия картинки. Проверьте формат")
			st.error(ex)

	col1, col2 = st.columns(2)
	with col1:
		st.image(uploaded_image, caption="Исходная картинка", use_column_width=True)
		
	# !!!!!!!!!!!! Здесь нужна наша модель для картинки
	
	model = YOLO('models/yolov8n.pt')
	
	with col2:
		res = model.predict(uploaded_image,	conf=confidence)
		boxes = res[0].boxes
		res_plotted = res[0].plot()[:, :, ::-1]
		st.image(res_plotted, caption='Результат модели',
				 use_column_width=True)		
	
	return



def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None):

	image = cv2.resize(image, (720, int(720*(9/16))))

	if is_display_tracking:
		res = model.track(image, conf=conf, persist=True, tracker=tracker)
	else:
		res = model.predict(image, conf=conf)

	res_plotted = res[0].plot()	
	st_frame.image(res_plotted,
				   caption='Видео с детекцией',
				   channels="BGR",
				   use_column_width="auto")
				   

def video_input(conf):
	
	## Загрузка видео
	uploaded_video = st.sidebar.file_uploader('Загрузите видео', type=[ "mp4", "mov",'avi','asf', 'm4v' ])
	
	DEFAULT_video = 'demo.mp4'
	tffile = tempfile.NamedTemporaryFile(suffix = '.mp4', delete=False)
	
	## отображение видео
	if not uploaded_video:
		vid = cv2.VideoCapture(DEFAULT_video)
		tffile.name = DEFAULT_video
		dem_vid = open(tffile.name, 'rb')
		demo_bytes = dem_vid.read()
		
		st.sidebar.text('Исходное видео')
		st.sidebar.video(demo_bytes)
	else:
		tffile.write(uploaded_video.read())
		dem_vid = open(tffile.name, 'rb')
		demo_bytes = dem_vid.read()
		
		st.sidebar.text('Исходное видео')
		st.sidebar.video(demo_bytes)
	

	# !!!!!!!!!!!! Здесь нужна наша модель для видео
	
	model = YOLO('models/yolov8n.pt')
	# кнопка Запустить
	if st.sidebar.button("Запустить детекцию"):
		try:
			vid_cap = cv2.VideoCapture(tffile.name)
			
			# для выравнивания видео по центру нужны колонки
			col1, col2, col3 = st.columns((2, 10, 2))
			with col2:
				st_frame = st.empty()
				while (vid_cap.isOpened()):
					success, image = vid_cap.read()
					if success:							
							_display_detected_frames(conf,model,st_frame,image)
					else:
						vid_cap.release()
						break
				

						
		except Exception as e:
			st.sidebar.error("Ошибка загрузки видео: " + str(e))
			
		kpi1, kpi2, kpi3 = st.columns(3)
		with kpi1:
			st.markdown('**Frame Rate**')
			kpi1_text = st.markdown('0')
			
		with kpi2:
			st.markdown('**Всего объектов**')
			kpi1_text = st.markdown('0')
			
		with kpi3:
			st.markdown('**Разрешение**')
			kpi1_text = st.markdown('0')
		
	return
	
	

def rtsp_stream(conf):

	source_rtsp = st.sidebar.text_input("Ссылка rtsp:")
	st.sidebar.caption('Пример ссылки: rtsp://rtsp:A1234567@188.170.176.190:8028/Streaming/Channels/101?transportmode=unicast&profile=Profile_1')
	
	# !!!!!!!!!!!! Здесь нужна наша модель для видео	
	model = YOLO('models/yolov8n.pt')
	
	# кнопка Запустить
	if st.sidebar.button("Запустить детекцию") and source_rtsp:
	
		try:
			vid_cap = cv2.VideoCapture(source_rtsp)
			st_frame = st.empty()
			while (vid_cap.isOpened()):
				success, image = vid_cap.read()
				if success:
					_display_detected_frames(conf,
											 model,
											 st_frame,
											 image)
				else:
					vid_cap.release()
					break
		except Exception as e:
			vid_cap.release()
			st.sidebar.error("Ошибка загрузки потока RTSP: " + str(e))
	

def main():

	st.set_page_config(
		page_title="ЛЦТ Видеодетекция вооруженных людей",
		layout="wide",
		initial_sidebar_state="expanded"
	)
	st.title('Видеодетекция вооруженных людей')
	
	st.sidebar.title('Настройки модели')

	
	# input options
	input_option = st.sidebar.radio("Выберите режим работы:", ['Картинка', 'Видео', 'Видеопоток (rtsp)'])
	
	confidence = st.sidebar.slider('Confidence', min_value=0.0, max_value=1.0, value=0.3)
	
	
	## Чек боксы
#	save_img = st.sidebar.checkbox('Save Video')
#	enable_GPU = st.sidebar.checkbox('enable_GPU')
	
#	st.sidebar.markdown('---')

	if input_option == 'Картинка':
		image_input(confidence)
	
	elif input_option == 'Видео':
		video_input(confidence)
		
	elif input_option == 'Видеопоток (rtsp)':
		rtsp_stream(confidence)
	

	
	st.sidebar.markdown('---')
	
	

if __name__ =='__main__':
	try:
		main()
	except SystemExit:
		pass
