FROM python:3.6
COPY . .

ENV JAVA_HOME /usr/lib/jvm/java-1.7-openjdk/jre
RUN apt-get update && apt-get install -y g++ default-jdk

RUN pip3 install -r requirements.txt

# RUN touch /usr/local/etc/mecabrc
# RUN touch /usr/local/lib/mecab/dic/mecab-ko-dic/dicrc

CMD [ "python3", "main.py" ]