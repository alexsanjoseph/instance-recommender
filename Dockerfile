FROM python:3.8.6

# Create a group and user
RUN useradd -ms /bin/bash recommender

USER recommender

WORKDIR /home/recommender

COPY . .

RUN pip install -r requirements.txt

CMD [ "/home/recommender/.local/bin/streamlit", "run", "streamlit_ui.py" ]
