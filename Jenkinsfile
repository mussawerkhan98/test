// Jenkinsfile - the pipeline recipe Jenkins follows on every build.
// Same idea as TripTick's pipeline: test -> build image -> deploy -> check -> clean up.
 
pipeline {
    agent any
 
    environment {
        IMAGE_NAME = 'hello-app'                 // name of our Docker image
        IMAGE_TAG  = "${BUILD_NUMBER}"           // dynamic tag: build 1, 2, 3...
        CONTAINER  = 'hello-app'                 // name of the running container
        NETWORK    = 'cicd-net'                  // Docker network shared with MongoDB
    }
 
    stages {
        stage('Checkout') {
            steps {
                // Jenkins has already pulled the code from GitHub; show what it got
                sh 'git log -1 --oneline'
            }
        }
 
        stage('Build image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }
 
        stage('Unit tests') {
            steps {
                // Run the tests inside the image we just built
                sh 'docker run --rm $IMAGE_NAME:$IMAGE_TAG python -m pytest -q'
            }
        }
 
        stage('Deploy') {
            steps {
                // The MongoDB connection string is a Jenkins secret, never in GitHub
                withCredentials([string(credentialsId: 'mongo-app-url', variable: 'MONGO_URL')]) {
                    sh '''
                        docker rm -f $CONTAINER || true
                        docker run -d --name $CONTAINER --network $NETWORK \
                          -p 5000:5000 \
                          -e MONGO_URL="$MONGO_URL" \
                          -e APP_VERSION="build-$IMAGE_TAG" \
                          $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }
 
        stage('Health check') {
            steps {
                // Wait, then ask the app if it is alive and connected to MongoDB
                sh '''
                    sleep 5
                    curl -fsS http://$CONTAINER:5000/health
                '''
            }
        }
    }
 
    post {
        success {
            echo "Deployed build ${BUILD_NUMBER} - open http://localhost:5000"
        }
        failure {
            echo 'Pipeline failed - read the red stage above'
        }
        always {
            // Clean up: delete old images, keep only the latest 3 (like Kareem's 'docker rmi')
            sh '''
                docker images $IMAGE_NAME --format '{{.Tag}}' | sort -n | head -n -3 | \
                  xargs -r -I{} docker rmi $IMAGE_NAME:{} || true
            '''
        }
    }
}