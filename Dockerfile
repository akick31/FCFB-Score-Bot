FROM python:3.10

# Create directories and copy over
RUN mkdir /project
WORKDIR /project
COPY ./requirements.txt ./
COPY . ./

# Install everything
RUN pip install -r requirements.txt

# Run
CMD [ "python", "FCFBScoreBot.py" ]