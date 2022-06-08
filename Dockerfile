FROM python:3.6
COPY . .

ENV JAVA_HOME /usr/lib/jvm/java-1.7-openjdk/jre
RUN apt-get update && apt-get install -y g++ default-jdk

RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py" ]