# set the base image to build from
FROM node:alpine

# set the working directory
WORKDIR /app

# copy package files
COPY package.json ./
COPY package-lock.json ./

# install dependencies
RUN npm install

# copy everything to /app directory
COPY ./ ./

# run the app
CMD ["npm", "start"]

